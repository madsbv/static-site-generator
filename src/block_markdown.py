#!/usr/bin/env python3

import re


def markdown_to_blocks(text):
    blocks = []
    current = ""
    for s in text.splitlines():
        if len(s.strip()) == 0:
            # s is a blank line separating blocks
            if len(current) > 0:
                # Only add the current block if it's non-empty
                blocks.append(current.strip())
                current = ""
            continue
        current += "\n" + s
    # Add the last block
    blocks.append(current.strip())
    return blocks


# Assumes that leading and trailing whitespace has been stripped
def block_to_block_type(block):
    if len(block) == 0:
        return "paragraph"

    # Check which block types it could be
    if len(re.findall(r"^#{1,6} ", block)) != 0:
        return "heading"
    elif len(re.findall(r"^```[\s\S]*```$", block)) != 0:
        return "code"
    elif block[0] == ">":
        quote = True
        for s in block.splitlines():
            if len(s) == 0 or s[0] != ">":
                quote = False
                break
        if quote:
            return "quote"
    elif block[0] == "*" or block[0] == "-":
        unordered_list = True
        for s in block.splitlines():
            s = s.strip()
            if len(s) == 0 or (s[0] != "*" and s[0] != "-"):
                unordered_list = False
                break
            if unordered_list:
                return "unordered_list"
    elif block[0] == "1":
        current_line = 1
        ordered_list = True
        for s in block.splitlines():
            if len(s) < 2 or s[0] != f"{current_line}" or s[1] != ".":
                ordered_list = False
                break
            current_line += 1
        if ordered_list:
            return "ordered_list"

    print(f"Here: {block}")
    return "paragraph"
