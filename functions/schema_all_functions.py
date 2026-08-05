from google import genai
from dotenv import load_dotenv
from google.genai import types
from functions.get_file_content import *
from functions.get_files_info import *
from functions.run_python_file import *
from functions.write_file import *
from functions.search_web import *
import os

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "working_directory": types.Schema(
                type = types.Type.STRING,
                description = "./calculator"
            )
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="read the contents of a or more specified files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description='File name relative to the current working directory. You can give either the full name with extension (e.g. calculator.py) or just the base name (e.g. calculator); if the extension is omitted, the function will search for a matching file with any extension in the working directory.'
            ),
            "working_directory": types.Schema(
                type = types.Type.STRING,
                description = "./calculator"
            )
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="run python files provided by the prompt",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The specific file names, relative to the working directory. ",
            ),
            "working_directory": types.Schema(
                type = types.Type.STRING,
                description = "./calculator"
            )
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write a or more specifc context to the file that's been provided. If the file is not provided, don't run this function",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file names, relative to the working directory. ",

            ),
            'content':types.Schema(
                type=types.Type.STRING,
                description="The specific content that the users want to write, usually enclosed by '' quoation ",

            ),
            "working_directory": types.Schema(
                type = types.Type.STRING,
                description = "./calculator"
            )

        },
    ),
)

schema_search_web = types.FunctionDeclaration(
    name='web_search',
    description = 'Searches the web for current information.',
    parameters = types.Schema(
        type= types.Type.OBJECT,
        properties = {
            "query" : types.Schema(
                type=types.Type.STRING,
                description = "Search query text",
            ),
            "num_results": types.Schema(
                type = types.Type.INTEGER,
                description = "number of maximum result",
            ),
        },
    ),
)



available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
        schema_search_web


    ]
)


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    

    dict_map ={
        "get_files_info" : get_files_info,
        'get_file_content': get_file_content,
        'run_python_file': run_python_file,
        'write_file': write_file,
        'web_search': web_search
    }

    result = dict_map[function_call_part.name](**function_call_part.args)
    if not result:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
)
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": result},
        )
    ],
)
        


    


   



