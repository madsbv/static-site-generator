#!/usr/bin/env python3
import os
import shutil


def main():
    copy_dir("static", "public")


def copy_dir(src, dst):
    # We only recurse into each directoy once, so removing here is valid
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    for entry in os.listdir(src):
        from_path = os.path.join(src, entry)
        to_path = os.path.join(dst, entry)
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        if os.path.isdir(from_path):
            copy_dir(from_path, to_path)


if __name__ == "__main__":
    main()
