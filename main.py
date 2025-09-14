import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types


def main():
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
    contents=messages)
    print()
    print(response.text)

    if verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}')
    


if __name__ == "__main__":
    main()
