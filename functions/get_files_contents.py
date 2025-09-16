MAX_CHARS = 10000
import os
def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    try:
        full_path = os.path.join(working_directory, file_path)

        if file_path.startswith('/') or file_path.startswith('..') or (os.path.abspath(full_path).startswith(os.path.abspath(working_directory))==False):
            return f'   Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        

        if not os.path.isfile(full_path):
            return f'   Error: File not found or is not a regular file: "{file_path}"'

    
        with open(full_path, 'r') as f:
            content = f.read()
            if len(content)>=MAX_CHARS:
                f.seek(0)
                return f.read(MAX_CHARS) + f'[...File {file_path} truncated at 10000 characters]'
            return content
    except Exception as e:
        print(f'    Error: {e}')


        
        


