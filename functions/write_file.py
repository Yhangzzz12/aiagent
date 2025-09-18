import os

def write_file(working_directory, file_path, content):
    file_full_path = os.path.join(working_directory, file_path)
    print(os.path.exists(file_full_path))

    if file_path.startswith('/') or file_path.startswith('..') or (os.path.abspath(file_full_path).startswith(os.path.abspath(working_directory))==False):
            return f'   Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(file_full_path):
        try:
            #If exist_ok is False (the default), a FileExistsError is raised if the target directory already exists.
            os.makedirs(os.path.dirname(file_full_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"

    

    try:
        with open(file_full_path,'w') as f:
            if content:
                new_content = f.write(content)
                return f'   Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        print(f'    Error: {e}')

                



