import os
import sys
import django
import pandas as pd
import openai
from typing import Dict, List
import json
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vocab_flashcards.settings')
django.setup()

from vocabulary.models import WordsBank, WordType, DifficultyLevel, WordList
from decouple import config

class VocabularyGenerator:
    def __init__(self):
        self.openai_api_key = config('OPENAI_API_KEY', default='')
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def generate_word_data(self, word: str) -> Dict:
        """Generate comprehensive word data using OpenAI GPT"""
        prompt = f"""
        Generate comprehensive vocabulary data for the word "{word}" in JSON format:
        {{
            "word": "{word}",
            "word_type": "noun/verb/adjective/adverb",
            "difficulty_level": "beginner/intermediate/advanced/expert",
            "meaning_english": "clear English definition",
            "meaning_urdu": "Urdu translation",
            "example_sentence": "example sentence using the word",
            "synonyms": "comma-separated synonyms",
            "antonyms": "comma-separated antonyms",
            "pronunciation": "phonetic pronunciation like /wɜːrd/"
        }}
        
        Make sure the Urdu translation is accurate and the difficulty level is appropriate for SAT vocabulary.
        """
        
        try:
            if not self.openai_api_key:
                return self._fallback_generation(word)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3
            )
            
            content = response.choices[0].message.content.strip()
            # Extract JSON from response
            start = content.find('{')
            end = content.rfind('}') + 1
            json_str = content[start:end]
            
            return json.loads(json_str)
        
        except Exception as e:
            print(f"Error generating data for {word}: {e}")
            return self._fallback_generation(word)
    
    def _fallback_generation(self, word: str) -> Dict:
        """Fallback method when OpenAI is not available"""
        return {
            "word": word,
            "word_type": "noun",
            "difficulty_level": "intermediate",
            "meaning_english": f"Definition for {word} (AI generation failed)",
            "meaning_urdu": f"{word} کا اردو معنی",
            "example_sentence": f"This is an example sentence with {word}.",
            "synonyms": "",
            "antonyms": "",
            "pronunciation": f"/{word.lower()}/"
        }
    
    def process_excel_file(self, file_path: str) -> List[Dict]:
        """Process Excel file and generate data for all words"""
        try:
            df = pd.read_excel(file_path)
            words_column = df.columns[0]  # First column
            words = df[words_column].dropna().tolist()
            
            generated_data = []
            total_words = len(words)
            
            print(f"Processing {total_words} words...")
            
            for i, word in enumerate(words, 1):
                print(f"Processing {i}/{total_words}: {word}")
                word_data = self.generate_word_data(str(word).strip())
                generated_data.append(word_data)
                
                # Rate limiting for API calls
                if self.openai_api_key:
                    time.sleep(1)  # 1 second delay between requests
            
            return generated_data
        
        except Exception as e:
            print(f"Error processing Excel file: {e}")
            return []
    
    def save_to_database(self, words_data: List[Dict]) -> int:
        """Save generated words to database"""
        saved_count = 0
        
        # Get or create default objects
        default_list, _ = WordList.objects.get_or_create(
            word_list_name="AI Generated",
            defaults={'description': 'Words generated using AI'}
        )
        
        for word_data in words_data:
            try:
                # Get or create word type
                word_type, _ = WordType.objects.get_or_create(
                    word_type=word_data['word_type'],
                    defaults={'abbreviation': word_data['word_type'][:3]}
                )
                
                # Get or create difficulty level
                difficulty, _ = DifficultyLevel.objects.get_or_create(
                    level=word_data['difficulty_level']
                )
                
                # Create word entry
                word_obj, created = WordsBank.objects.get_or_create(
                    word=word_data['word'],
                    defaults={
                        'word_type': word_type,
                        'difficulty_level': difficulty,
                        'meaning_english': word_data['meaning_english'],
                        'meaning_urdu': word_data['meaning_urdu'],
                        'example_sentence': word_data['example_sentence'],
                        'synonyms': word_data['synonyms'],
                        'antonyms': word_data['antonyms'],
                        'pronunciation': word_data['pronunciation'],
                    }
                )
                
                if created:
                    word_obj.word_lists.add(default_list)
                    saved_count += 1
                    print(f"✓ Saved: {word_data['word']}")
                else:
                    print(f"- Exists: {word_data['word']}")
            
            except Exception as e:
                print(f"✗ Error saving {word_data['word']}: {e}")
        
        return saved_count

def main():
    if len(sys.argv) != 2:
        print("Usage: python word_generator.py <excel_file_path>")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    
    if not os.path.exists(excel_file):
        print(f"Error: File {excel_file} not found")
        sys.exit(1)
    
    generator = VocabularyGenerator()
    
    # Process Excel file
    print("Starting vocabulary generation...")
    words_data = generator.process_excel_file(excel_file)
    
    if not words_data:
        print("No data generated. Exiting.")
        sys.exit(1)
    
    # Save to database
    print("\nSaving to database...")
    saved_count = generator.save_to_database(words_data)
    
    print(f"\n✅ Process completed!")
    print(f"📊 Total words processed: {len(words_data)}")
    print(f"💾 Words saved to database: {saved_count}")

if __name__ == "__main__":
    main()