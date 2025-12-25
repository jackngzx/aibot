import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import available_functions

parser = argparse.ArgumentParser(description="Aibot parser")
parser.add_argument("user_prompt", type=str, help="What is a user prompt?")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("API key not found")

client = genai.Client(api_key=api_key)


def main():
    print("Hello from aibot!")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    usage = response.usage_metadata
    if response.usage_metadata is None:
        raise RuntimeError("Failed API request")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")
    if response.function_calls is not None:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
