import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    print("Hello from aibot!")
    parser = argparse.ArgumentParser(description="Aibot parser")
    parser.add_argument("user_prompt", type=str, help="What is a user prompt?")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    MAX_ITERS = 20
    for _ in range(MAX_ITERS):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations ({MAX_ITERS}) reached")
    sys.exit(1)


def generate_content(client, messages, verbose):
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

    if verbose:
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_results = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose)
        if function_call_result.parts is None:
            raise Exception("Empty function_call_result.parts")
        if function_call_result.parts[0].function_response is None:
            raise Exception(".function_response property is None")
        if function_call_result.parts[0].function_response.response is None:
            raise Exception(".function_response.response is None")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_results.append(function_call_result.parts[0])
    messages.append(types.Content(role="user", parts=function_results))


if __name__ == "__main__":
    main()
