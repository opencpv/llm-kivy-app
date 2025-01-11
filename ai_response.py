import requests
import json
import os 
def send_chat_message(message, user_profile=None, model="openai/gpt-3.5-turbo", api_key=""):
   
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    
    # Create context from user profile
    context = ""
    if user_profile:
        context = "User Profile Information:\n"
        for key, value in user_profile.items():
            if value:  # Only include non-empty fields
                context += f"- {key}: {value}\n"
        context += "\nPlease consider this information when responding to: "
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful healthcare assistant. Provide personalized advice based on the user's profile information when available."
            },
            {
                "role": "user",
                "content": f"{context}{message}" if context else message
            }
        ]
    }
    
    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(payload)
    )
    print(response.json())
    return response.json()