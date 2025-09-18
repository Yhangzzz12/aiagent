import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types
from functions.schema_all_functions import *
from functions.schema_all_functions import available_functions



def main():
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
Be sure to explain how did you finish the process after each call
"""
    argv = sys.argv[1:]
    verbose = "--verbose" in argv
    if not argv:
        print(f'the format is [uv run main.py] [text input]')
        sys.exit(1)
    
    if verbose:
        
        print (f'User prompt: {sys.argv[1]}')
    
    messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
]
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")


    client = genai.Client(api_key=api_key)
    
    #Generate Contents
    response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(tools = [available_functions],system_instruction=system_prompt),
    
)
    print()
    if response.function_calls:
        for fc in response.function_calls: 
               # fc is a genai.types.FunctionCall
            call_result = call_function(fc, verbose=True)
            if not call_result:
                raise Exception('An Error')
            else:
                print(f"-> {call_result.parts[0].function_response.response}")

    
    else:
        print(response.text)

    if verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}')
    


if __name__ == "__main__":
    main()
