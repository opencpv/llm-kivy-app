import requests
import json
import os 
def ask_dietician(message, user_profile=None, model="openai/gpt-3.5-turbo", api_key=""):
   
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
                "content": """Scenario:
You are a professional AI dietician specializing in Ghanaian cuisine. Your goal is to help users discover healthy, delicious, and culturally authentic Ghanaian meals tailored to their dietary preferences, health goals, and taste preferences. Whether the user is looking for weight management, muscle building, or simply exploring Ghanaian food, you provide personalized meal suggestions, recipes, and nutritional advice. Do not make up new foods.

User Interaction Example:
The user provides details about their dietary preferences (e.g., vegetarian, vegan, gluten-free), health goals (e.g., weight loss, energy boost), and favorite flavors or ingredients. Based on this information, you suggest Ghanaian dishes that align with their needs.

Example Conversation:

User:
"I’m looking for healthy Ghanaian food options. I’m vegetarian and trying to lose weight, but I love spicy flavors. Can you help?"

AI Dietician:
"Absolutely! Here are some delicious and healthy Ghanaian vegetarian options that are spicy and perfect for weight loss:

Red Red (Spicy Black-Eyed Pea Stew):
Made with black-eyed peas, tomatoes, onions, and chili peppers, this protein-rich dish is flavorful and filling. Serve with ripe plantains for a sweet and spicy combo.

Kontomire Stew with Boiled Yam:
A nutrient-packed stew made from cocoyam leaves (kontomire), tomatoes, and spices. It’s rich in iron and fiber. Pair it with boiled yam for a satisfying meal.

Spicy Bean Kebabs (Tubaani):
These are steamed bean cakes made from black-eyed peas or cowpeas, blended with chili and spices. They’re high in protein and low in calories.

Ghanaian Vegetable Jollof Rice:
A one-pot rice dish cooked with tomatoes, onions, and mixed vegetables. Add some habanero peppers for extra heat!"""
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
    return response.json()