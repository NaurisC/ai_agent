import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns truncated (1000 characters max)  contents of a file as a string.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file, to extract contents from, relative to the working directory.",
                },
            },
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_file_path = (
        os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
    )

    if valid_target_file_path == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif os.path.isfile(target_file_path) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    else:

        try:
            with open(target_file_path, "r") as f:
                file_content_string = f.read(MAX_CHARS)
                trunc_check = f.read(1)
        except Exception as e:
            return f"Error: {e}"

        if trunc_check != "":
            file_content_string += (
                f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            )
        return file_content_string
