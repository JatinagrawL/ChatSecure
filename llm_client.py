import requests
import json
import logging
from typing import Optional, Dict, Any

class LLMClient:
    """Client for communicating with various LLM APIs"""
    
    def __init__(self, api_key: str, endpoint: str, provider: str = 'openai'):
        self.api_key = api_key
        self.endpoint = endpoint
        self.provider = provider.lower()
        self.session = requests.Session()
        
        # Set up headers based on provider
        if self.provider == 'openai':
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            })
        elif self.provider == 'anthropic':
            self.session.headers.update({
                'x-api-key': api_key,
                'Content-Type': 'application/json',
                'anthropic-version': '2023-06-01'
            })
        else:
            # Generic setup for custom providers
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            })
    
    def test_connection(self) -> bool:
        """Test if the API connection is working"""
        try:
            response = self.send_message("Hello", test_mode=True)
            return response is not None
        except Exception as e:
            logging.error(f"Connection test failed: {str(e)}")
            return False
    
    def send_message(self, message: str, test_mode: bool = False) -> Optional[str]:
        """Send message to LLM and return response"""
        try:
            if self.provider == 'openai':
                return self._send_openai_message(message, test_mode)
            elif self.provider == 'anthropic':
                return self._send_anthropic_message(message, test_mode)
            else:
                return self._send_generic_message(message, test_mode)
        except Exception as e:
            logging.error(f"Error sending message to {self.provider}: {str(e)}")
            return None
    
    def _send_openai_message(self, message: str, test_mode: bool = False) -> Optional[str]:
        """Send message to OpenAI API"""
        test_message = "Hi" if test_mode else message
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": test_message}
            ],
            "max_tokens": 150 if test_mode else 1000,
            "temperature": 0.7
        }
        
        try:
            response = self.session.post(self.endpoint, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content'].strip()
            
        except requests.exceptions.RequestException as e:
            logging.error(f"OpenAI API request failed: {str(e)}")
        except KeyError as e:
            logging.error(f"Unexpected OpenAI API response format: {str(e)}")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse OpenAI API response: {str(e)}")
        
        return None
    
    def _send_anthropic_message(self, message: str, test_mode: bool = False) -> Optional[str]:
        """Send message to Anthropic API"""
        test_message = "Hi" if test_mode else message
        
        payload = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 150 if test_mode else 1000,
            "messages": [
                {"role": "user", "content": test_message}
            ]
        }
        
        try:
            response = self.session.post(self.endpoint, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if 'content' in data and len(data['content']) > 0:
                return data['content'][0]['text'].strip()
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Anthropic API request failed: {str(e)}")
        except KeyError as e:
            logging.error(f"Unexpected Anthropic API response format: {str(e)}")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse Anthropic API response: {str(e)}")
        
        return None
    
    def _send_generic_message(self, message: str, test_mode: bool = False) -> Optional[str]:
        """Send message to generic/custom API"""
        test_message = "Hi" if test_mode else message
        
        # Try OpenAI format first
        payload = {
            "model": "default",
            "messages": [
                {"role": "user", "content": test_message}
            ],
            "max_tokens": 150 if test_mode else 1000,
            "temperature": 0.7
        }
        
        try:
            response = self.session.post(self.endpoint, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Try OpenAI format
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content'].strip()
            
            # Try Anthropic format
            if 'content' in data and len(data['content']) > 0:
                return data['content'][0]['text'].strip()
            
            # Try simple response format
            if 'response' in data:
                return data['response'].strip()
            
            # Try text field
            if 'text' in data:
                return data['text'].strip()
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Generic API request failed: {str(e)}")
        except KeyError as e:
            logging.error(f"Unexpected API response format: {str(e)}")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse API response: {str(e)}")
        
        return None
