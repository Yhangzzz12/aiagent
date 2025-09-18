import os
from google import genai
from dotenv import load_dotenv
from google.genai import types


def get_files_info(working_directory, directory="."):
    
    '''The directory parameter should be treated as a relative path within the working_directory. 
    Use os.path.join(working_directory, directory) to create the full path, 
    then validate it stays within the working directory boundaries.'''
    full_path = os.path.join(working_directory, directory)


    if directory.startswith('/') or directory.startswith('..') or (os.path.abspath(full_path).startswith(os.path.abspath(working_directory))==False):
        return f'   Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if os.path.isfile(directory):
        return f'   Error:{directory} is not a directory'

    # means if os didn't find that specific dir in working directory
    if not os.path.isdir(full_path):
        return f'   Error: "{full_path}" is not a directory or you may type wrong'

    


    
    content_of_dir = ''
    for content in os.listdir(full_path):
        content_of_dir += f'-{content}: file_size={os.path.getsize(os.path.join(full_path,content))} bytes, is_dir={os.path.isdir(os.path.join(full_path,content))}\n'
    return content_of_dir
    
    


    
