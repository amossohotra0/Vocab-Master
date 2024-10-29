# AI Vocabulary Generator

Automatically generate comprehensive vocabulary data from Excel word lists using OpenAI GPT.

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r ai_tools/requirements.txt
   ```

2. **Configure OpenAI API:**
   Add to your `.env` file:
   ```env
   OPENAI_API_KEY=your-openai-api-key-here
   ```

3. **Get OpenAI API Key:**
   - Go to [OpenAI Platform](https://platform.openai.com/)
   - Create account and get API key
   - Add billing information (required for API usage)

## Usage

### 1. Prepare Excel File
Create an Excel file with words in the first column:
```
Word
aberrant
abscond
acumen
...
```

### 2. Run Generator
```bash
python ai_tools/word_generator.py path/to/your/words.xlsx
```

### 3. Generated Data
For each word, the AI generates:
- **Word Type:** noun, verb, adjective, adverb
- **Difficulty Level:** beginner, intermediate, advanced, expert
- **English Meaning:** Clear definition
- **Urdu Translation:** Accurate Urdu meaning
- **Example Sentence:** Contextual usage
- **Synonyms:** Related words
- **Antonyms:** Opposite words
- **Pronunciation:** Phonetic guide

## Features

- **Batch Processing:** Handle hundreds of words at once
- **Rate Limiting:** Respects OpenAI API limits
- **Fallback Mode:** Works without API key (basic data)
- **Database Integration:** Automatically saves to Django database
- **Duplicate Handling:** Skips existing words
- **Progress Tracking:** Shows processing status

## Cost Estimation

OpenAI GPT-3.5-turbo pricing (approximate):
- **100 words:** ~$0.50
- **500 words:** ~$2.50
- **1000 words:** ~$5.00

## Example Output

```json
{
    "word": "aberrant",
    "word_type": "adjective",
    "difficulty_level": "advanced",
    "meaning_english": "departing from an accepted standard",
    "meaning_urdu": "غیر معمولی، منحرف",
    "example_sentence": "His aberrant behavior worried his friends.",
    "synonyms": "abnormal, deviant, unusual",
    "antonyms": "normal, typical, standard",
    "pronunciation": "/ˈæbərənt/"
}
```

## Troubleshooting

### No OpenAI API Key
- Generator will use fallback mode
- Basic data structure created
- Manual editing required

### API Rate Limits
- Built-in 1-second delay between requests
- Upgrade OpenAI plan for higher limits

### Excel File Issues
- Ensure first column contains words
- Remove empty rows
- Use .xlsx format

## Alternative AI Services

If OpenAI is not available, you can modify the code to use:
- **Google Gemini API**
- **Anthropic Claude API**
- **Local LLM models (Ollama)**

## Sample Usage

```bash
# Test with sample file
python ai_tools/word_generator.py ai_tools/sample_words.xlsx

# Process your word list
python ai_tools/word_generator.py my_vocabulary_list.xlsx
```