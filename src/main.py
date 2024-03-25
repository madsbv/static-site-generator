#!/usr/bin/env python3
import os
import shutil

from block_markdown import extract_title, markdown_to_html_node


def main():
    copy_dir("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


def generate_page(src, tmpl, dst):
    print(f"Generating page from {src} to {dst} using {tmpl}")
    with open(src) as m:
        md = m.read()
    with open(tmpl) as t:
        template = t.read()

    title = extract_title(md)
    html = markdown_to_html_node(md).to_html()
    result = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # Extract the parent directory of dst
    dst_dir = "/".join(dst.split("/")[:-1])
    # We just accept errors if dst_dir already exists as a file
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    with open(dst, "w") as out_file:
        out_file.write(result)


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
