import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = (
        os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    )

    if valid_target_dir == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif os.path.isdir(target_dir) != True:
        return f'Error "{target_dir}" is not a directory'
    else:

        #       return f'- {"\n- ".join(os.listdir(os.path.getsize(directory)))}'
        files = []
        for dir in os.listdir(target_dir):
            dir_path = str(target_dir) + "/" + str(dir)
            files.append(
                f"- {dir}: file_size={os.path.getsize(dir_path)} bytes, is_dir={os.path.isdir(dir_path)}"
            )
        return "\n".join(files)
