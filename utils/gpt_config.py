import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")
MODEL = "gpt-3.5-turbo"

client = OpenAI(
    api_key = OPENAI_KEY
)

def get_answer(prompt: str):
    response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
    
    return response.choices[0].message.content