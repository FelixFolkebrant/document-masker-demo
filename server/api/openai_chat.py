import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(organization="org-sXMg36FtwtvWOC71TH6ida3r", api_key=API_KEY)

def get_chat_response(prompt: str, instructions: str) -> str:
    print(instructions)
    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content


