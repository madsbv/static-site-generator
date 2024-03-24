#!/usr/bin/env python3
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
