import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import json
import sys

parser = argparse.ArgumentParser(description="Milhouse")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key == None:
    raise RuntimeError("No key found")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages = [
    {"role": "system", "content": system_prompt},
    {
        "role": "user",
        "content": args.user_prompt,
    },
]

for _ in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    if response.usage == None:
        raise RuntimeError("Failed API request")
    elif args.verbose:
        print(
            f"User prompt: {args.user_prompt}\nPrompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}"
        )
    else:
        pass

    # print(response.choices[0].message.content)

    message = response.choices[0].message
    print(f"message: {message}")
    messages.append(message)
    print(f"MESSAGES: {messages}")

    if message.tool_calls != None:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            messages.append(result_message)
            if not result_message["content"]:
                raise Exception("Empty content")
            elif args.verbose == True:
                print(f"-> {result_message['content']}")
    else:
        print(message.content)
        break
else:
    print(f"Maximum iterations reached")
    sys.exit(1)

# def main():
#    print("Hello from milhouse!")


# if __name__ == "__main__":
#    main()
