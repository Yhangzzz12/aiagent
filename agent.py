# agent.py
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.schema_all_functions import *
from functions.schema_all_functions import available_functions
from typing import List
from urllib.request import urlopen

load_dotenv()

SYSTEM_PROMPT = """
You are a helpful AI agent.
If the user asks about files or code (e.g., list/read/write/execute), plan and use the available tools.
If the request is general (no file operations needed), answer directly without tools.
If the user asks about a definition, a meaning, or uses words like search/find/look up, you may call the search_web tool. 
When the request is general saying 'hello', being yourself as a nature chill guy and repsonses some easy chill sentences.
"""

API_KEY = os.environ.get("GEMINI_API_KEY")

# Return type is a plain string. Discord will send this back to users.
def run_agent(prompt: str, verbose: bool = False) -> str:


    if not API_KEY:
        return "ERROR: GEMINI_API_KEY is not set."

    client = genai.Client(api_key=API_KEY)

    prev: List[types.Content] = getattr(run_agent, "_history", [])
    messages = list(prev)  # start from previous turns

    messages.append(types.Content(role="user", parts=[types.Part(text=prompt)]))
    final_text = ""

    for _ in range(20):
        # Model step
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=SYSTEM_PROMPT
            ),
        )

        # Persist the model message(s) to the conversation
        for resp in response.candidates:
            messages.append(resp.content)

        dict_map ={
        "get_files_info" : get_files_info,
        'get_file_content': get_file_content,
        'run_python_file': run_python_file,
        'write_file': write_file,
        'web_search': web_search
    }

        # Tool-use path
        if response.function_calls:
            '''print(response.function_calls)
            print(response.function_calls[0].name)'''
            function_calls_parts = []
            for fc in response.function_calls:
                try:
                    call_result = call_function(fc, verbose)
                    if fc.name == "web_search":
                        results = dict_map[fc.name](**fc.args)
                        final_text += f'{results}\n-------------------------------\nIn Summary:\n\n'
                    if not call_result:
                        return "ERROR: A function call failed with no result."
                    # Persist the tool response back to the model
                    function_calls_parts.append(call_result.parts[0])
                except Exception as e:
                    return f"ERROR while executing tool `{fc.name}`: {e}"

            messages.append(types.Content(role="user", parts=function_calls_parts))
            # loop continues so model can read tool outputs
            continue

        # Text path (done)
        final_text += response.text or ""
        if verbose:
            pt = response.usage_metadata.prompt_token_count
            rt = response.usage_metadata.candidates_token_count
            final_text += f"\n\n[usage] prompt_tokens={pt}, response_tokens={rt}"
        break


        
    # after you set final_text (inside your loop) and before return:
    if final_text:
        messages.append(types.Content(role="model", parts=[types.Part(text=final_text)]))

    # keep history for next call (trim so it doesn't grow forever)
    run_agent._history = messages[-40:]

    return final_text or "I ran the tools, but the model didn’t produce a final message."

print(run_agent('help me search the meaning of chair', False))