import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    file_full_path = os.path.join(working_directory, file_path)

    if file_path.startswith('/') or file_path.startswith('..') or (os.path.abspath(file_full_path).startswith(os.path.abspath(working_directory))==False):
        return f'   Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(file_full_path):
        return f'   Error: File "{file_path}" not found.'

    if not file_full_path.endswith('py'):
        return f'   Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(['python3', file_full_path, *args],timeout = 30, capture_output = True, text = True)
        if result.returncode != 0:
            return f'Process exited with code {result.returncode}'
        
        stdout = result.stdout
        stderr = result.stderr
        

        if stdout!=None and stderr!=None:
            return f'STDOUT:{stdout}\nSTDERR:{stderr}'
            
        else:
            return f'No output produced.'
    except Exception as e:
        return f"Error: executing Python file: {e}"

        


        
    


