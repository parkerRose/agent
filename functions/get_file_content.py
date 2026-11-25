import os
from config import *

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Gets the contents of a file given its path relative to the working directory, providing the first 10000 characters, or to the end of the file, whichever comes first.",
        "parameters": {
            "type": "object",
            "properties":{
                "file_path": {
                    "type": "string",
                    "description": "File path to get content of",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        file_abs_path = os.path.join(working_directory, file_path)
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted directory'
        if not os.path.isfile(file_abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(file_abs_path, 'r') as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters'
        return content
    except Exception as e:
        return f'Error: {e}'
