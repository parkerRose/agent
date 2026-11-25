import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Writes new file and overwrites existing files",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to get content of",
                },
                "args": {
                    "type": "array",
                    "items": {
                      "type": "string",
                    },
                    "description": "Additional arguments, optional",
                },
            },
        },
    },
}
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_abs_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_abs_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", file_abs_path]
        if args: command.extend(args)
        # print(file_abs_path)
        py_output = subprocess.run(command, capture_output= True, timeout = 30, cwd = working_dir_abs, text = True)
        output = ""
        if py_output.returncode != 0:
            output += f"Process exited with code {py_output.returncode}\n"
        if not py_output.stdout and not py_output.stderr:
            output += "No output produced"
            return output
        output += f"STDOUT: {py_output.stdout}"
        output += f"\nSTDERR: {py_output.stderr}"
        return output
    except Exception as e:
        return(f"Error: {e}")
