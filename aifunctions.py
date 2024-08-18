# aifunctions.py

import os
import openai

# Retrieve API key from environment variable
API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client
openai.api_key = API_KEY
client = openai.OpenAI()

def analyze_image_and_prompt(image_url, prompt):
    # Prepare the request to GPT-4o-mini
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    
    if response.choices and response.choices[0].message:
        print(response.choices[0].message['content'])
        return response.choices[0].message['content']
    else:
        return {'error': 'Failed to analyze the image and prompt.'}

def generate_dalle_image(analysis):
    # Prepare the request to DALL-E (Note: This is just a placeholder as DALL-E integration is not directly with openai client)
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    json_data = {
        'prompt': analysis,
        'n': 1,
        'size': '1024x1024'
    }
    
    response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=json_data)
    
    if response.status_code == 200:
        return response.json()['data'][0]['url']
    else:
        return {'error': 'Failed to generate image using DALL-E.'}
