import os
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes new file and overwrites existing files",
        "parameters": {
            "type": "object",
            "properties": {
                "required" : ["file_path", "content"],
                "file_path": {
                    "type": "string",
                    "description": "File path to get content of",
                },
                "content": {
                    "type": "string",
                    "description": "What content to write / overwrite into the file",
                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        file_abs_path = os.path.join(working_directory, file_path)
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted directory'
        os.makedirs(os.path.dirname(file_abs_path), exist_ok = True)
        with open(file_abs_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return(f"Error: {e}")
