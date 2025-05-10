from openai import OpenAI
import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

def get_openai_client():
    """Create and return an OpenAI client using the API key from environment variables"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    return OpenAI(api_key=api_key)

def generate_response(model: str = "gpt-4o-mini", messages: Optional[List[Dict[str, str]]] = None, 
                      temperature: float = 0, json_response: bool = False) -> Dict[str, Any]:
    """
    Generate a response using the OpenAI API
    
    Args:
        model (str): The model to use for generating the response
        messages (list): List of message dictionaries with role and content
        temperature (float): Temperature for response generation
        json_response (bool): Whether to request JSON response format
    
    Returns:
        dict: Response data including the generated content and token usage
    """
    if messages is None:
        messages = []
    
    client = get_openai_client()
    
    kwargs = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }
    
    if json_response:
        kwargs["response_format"] = {"type": "json_object"}
    
    try:
        response = client.chat.completions.create(**kwargs)
        return {
            "response": response.choices[0].message.content,
            "output_token": response.usage.completion_tokens,
            "input_token": response.usage.prompt_tokens
        }
    except Exception as e:
        raise RuntimeError(f"Error generating response: {str(e)}")
