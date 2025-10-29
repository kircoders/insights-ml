from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are a data analyst assistant. "
                "Only answer questions that relate to the dataset and its analysis. "
                "If a question is unrelated to the dataset, respond with: "
                "'Sorry, I can only answer questions about the uploaded dataset.'"
            )},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
