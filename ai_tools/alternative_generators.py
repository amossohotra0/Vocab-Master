"""
Alternative AI generators for vocabulary data
Use these if OpenAI is not available or preferred
"""

import requests
import json
from typing import Dict

class GeminiGenerator:
    """Google Gemini API generator"""
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    def generate_word_data(self, word: str) -> Dict:
        prompt = f"Generate vocabulary data for '{word}' in JSON format with fields: word, word_type, difficulty_level, meaning_english, meaning_urdu, example_sentence, synonyms, antonyms, pronunciation"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                # Extract JSON from response
                start = content.find('{')
                end = content.rfind('}') + 1
                return json.loads(content[start:end])
        except:
            pass
        
        return self._fallback_data(word)

class ClaudeGenerator:
    """Anthropic Claude API generator"""
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1/messages"
    
    def generate_word_data(self, word: str) -> Dict:
        prompt = f"Generate vocabulary data for '{word}' in JSON format with fields: word, word_type, difficulty_level, meaning_english, meaning_urdu, example_sentence, synonyms, antonyms, pronunciation"
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 500,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            if response.status_code == 200:
                content = response.json()["content"][0]["text"]
                start = content.find('{')
                end = content.rfind('}') + 1
                return json.loads(content[start:end])
        except:
            pass
        
        return self._fallback_data(word)

class OllamaGenerator:
    """Local Ollama generator"""
    def __init__(self, model: str = "llama2"):
        self.model = model
        self.base_url = "http://localhost:11434/api/generate"
    
    def generate_word_data(self, word: str) -> Dict:
        prompt = f"Generate vocabulary data for '{word}' in JSON format with fields: word, word_type, difficulty_level, meaning_english, meaning_urdu, example_sentence, synonyms, antonyms, pronunciation"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, json=payload)
            if response.status_code == 200:
                content = response.json()["response"]
                start = content.find('{')
                end = content.rfind('}') + 1
                return json.loads(content[start:end])
        except:
            pass
        
        return self._fallback_data(word)
    
    def _fallback_data(self, word: str) -> Dict:
        return {
            "word": word,
            "word_type": "noun",
            "difficulty_level": "intermediate",
            "meaning_english": f"Definition for {word}",
            "meaning_urdu": f"{word} کا معنی",
            "example_sentence": f"Example with {word}.",
            "synonyms": "",
            "antonyms": "",
            "pronunciation": f"/{word}/"
        }