import os


def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir])
    if valid_target_dir != working_dir_abs:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{target_dir}" is not a directory'
    with os.scandir(target_dir) as entries:
        files_info = []
        for entry in entries:
            file_name = entry.name
            full_path = os.path.join(target_dir, entry.name)
            file_size = os.path.getsize(full_path)
            file_or_dir = os.path.isdir(full_path)
            files_info.append(
                f"- {file_name}: file_size={file_size} bytes, is_dir={file_or_dir}"
            )
        return "\n".join(files_info)
