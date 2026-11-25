import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from call_function import *
from prompts import *
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type = str, help="User prompt")
parser.add_argument("--verbose", action="store_true",help="Enable verbose output")
args = parser.parse_args()

def main():


    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for i in range(MAX_TURNS):
        response = generate_content(client, messages)
        message = response.choices[0].message
        if message.content:
            print(message.content)
        messages.append(message)
        results: list[dict] = call_tools(message)
        messages.extend(results)

        if not results:
            break
    else:
        print("Error: reached max turn count without final response.")
        sys.exit(1)


    if args.verbose:
        print(f"User prompt: {args.user_prompt}\nPrompt tokens: {response.usage.prompt_tokens}\n Response tokens: {response.usage.completion_tokens}")

def generate_content(client, messages):
    response = client.chat.completions.create(
        model="openai/gpt-6-luna",
        messages= messages,
        tools= available_functions
    )
    return response

def call_tools(message: ChatCompletionMessage):
    results: list[dict]= []
    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_dict = {}
            result_dict = call_function(tool_call)
            if not result_dict["content"]:
                raise Exception("Empty output")
            if args.verbose:
                print(f"-> {result_dict['content']}")
            results.append(result_dict)
    return results


if __name__ == "__main__":
    main()
