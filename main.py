import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type = str, help="User prompt")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "user", "content": args.user_prompt},
    ]
    response = generate_content(client, messages)

    print(response.choices[0].message.content)
    print(f"Prompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")

def generate_content(client, messages):
    response = client.chat.completions.create(
        model="openai/gpt-6-luna",
        messages= messages
    )
    return response

if __name__ == "__main__":
    main()
