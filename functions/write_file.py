import os
from os.path import abspath

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Appends file with the content passed as argument",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to be written to. Relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": " Content that should be appended to the file passed as an argument",
                },
            },
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_file_path = (
        os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
    )

    if valid_target_file_path == False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    elif os.path.isdir(target_file_path) == True:
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    else:
        folder = os.path.dirname(target_file_path)
        os.makedirs(folder, mode=0o777, exist_ok=True)

        try:
            with open(target_file_path, "w") as f:
                f.write(content)
        except Exception as e:
            return f"error: {e}"

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
