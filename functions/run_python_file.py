import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes python file defined in the funciton parameters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to be executed (relative to the working directory)",
                },
                "args": {
                    "type": "string",
                    "description": "Optional list of arguments to be passed along with the execution command",
                },
            },
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_file_path = (
        os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
    )

    if valid_target_file_path == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif os.path.isfile(target_file_path) == False:
        return f'Error: "{file_path}" does not exist or is not a regular file'
    elif target_file_path.endswith(".py") == False:
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file_path]

    if args != None:
        command.extend(args)

    output = subprocess.run(
        command, cwd=working_directory, capture_output=True, timeout=30, text=True
    )
    try:
        if output.returncode != 0:
            return f"Process exited with code {output.returncode}"
        elif output.stdout == "" and output.stderr == "":
            return "No output produced"
        else:
            return f"STDOUT: {output.stdout}\nSTDERR:{output.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
