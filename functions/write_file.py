import os


def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_file = os.path.commonpath([working_dir_abs, target_file])
    if valid_target_file != working_dir_abs:
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    target_dir = os.path.dirname(target_file)
    if target_dir:
        os.makedirs(target_dir, exist_ok=True)
    with open(target_file, "w") as f:
        f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
