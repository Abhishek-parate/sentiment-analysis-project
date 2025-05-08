import os
import json
import re
import requests
from config import Config

class SentimentAnalyzer:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = "llama3-8b-8192"  # Using Llama 3 model through Groq
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
    
    def analyze(self, text):
        """
        Analyze the sentiment of the provided text using Groq API directly.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            dict: A dictionary containing sentiment analysis results
                {
                    'sentiment': 'positive' | 'negative' | 'neutral',
                    'score': float,  # confidence score between -1 and 1
                    'explanation': str  # brief explanation of the sentiment
                }
        """
        if not text or not text.strip():
            return {
                'sentiment': 'neutral',
                'score': 0.0,
                'explanation': 'No text provided for analysis.'
            }
        
        # Prompt for the LLM to analyze sentiment
        system_message = "You are a sentiment analysis assistant. Your task is to analyze the sentiment of text and return JSON with sentiment, score, and a brief explanation."
        
        user_prompt = f"""
        Please analyze the sentiment of the following text and respond with ONLY a JSON object with the following structure:
        {{
            "sentiment": "positive" or "negative" or "neutral",
            "score": a number between -1 and 1 where -1 is very negative, 0 is neutral, and 1 is very positive,
            "explanation": a one-sentence explanation of why the text has this sentiment
        }}

        Text to analyze: "{text}"
        
        JSON:
        """
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.1,
            "max_tokens": 200
        }
        
        try:
            # Call Groq API directly with requests
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise exception for non-2xx responses
            
            data = response.json()
            response_text = data['choices'][0]['message']['content'].strip()
            
            # Try to extract JSON if it's embedded in other text
            json_match = re.search(r'({.*})', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
                
            result = json.loads(response_text)
            
            # Ensure all expected fields are present
            if 'sentiment' not in result or 'score' not in result or 'explanation' not in result:
                raise ValueError("Missing fields in result")
                
            return result
            
        except Exception as e:
            # Fallback response in case of errors
            error_message = str(e)
            print(f"Error during sentiment analysis: {error_message}")
            return {
                'sentiment': 'neutral',
                'score': 0.0,
                'explanation': f'Error during analysis: {error_message}'
            }