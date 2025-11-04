from openai import OpenAI
import os

# Only load .env locally, not in CI
if os.getenv("ENV", "development") == "development":
    from dotenv import load_dotenv
    load_dotenv()

# This will raise an error if the key is missing (good!)
api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)

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
