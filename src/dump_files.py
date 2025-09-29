import os
from shutil import rmtree, copy


def move_all_files(source_dir: str, dest_dir: str) -> None:
    if not os.path.exists(source_dir):
        raise ValueError("source directory doesn't exist")

    if os.path.exists(dest_dir):
        rmtree(dest_dir)
    os.mkdir(dest_dir)
    for object in os.listdir(source_dir):
        from_path = os.path.join(source_dir, object)
        to_path = os.path.join(dest_dir, object)
        if os.path.isfile(from_path):
            copy(from_path, to_path)
        else:
            move_all_files(from_path, to_path)
    return
