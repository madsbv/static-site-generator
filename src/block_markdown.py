#!/usr/bin/env python3

import re

from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes


def markdown_to_html_node(text):
    blocks = markdown_to_blocks(text)
    outer = ParentNode("div", [])
    for b in blocks:
        outer.children.append(block_to_html_node(b))
    return outer


def block_to_html_node(block):
    type = block_type(block)
    match type:
        case "heading":
            i = 0
            while block[i] == "#":
                i += 1
            return ParentNode(f"h{i}", text_to_htmlnodes(block[i + 1 :]))
        case "code":
            return LeafNode("pre", block[3:-3])
        case "quote":
            text = ""
            for l in block.splitlines():
                text += l[1:] + "\n"
            return ParentNode("blockquote", text_to_htmlnodes(text))
        case "unordered_list":
            # NOTE: This is kind of crude in splitting away leading whitespace and indenting. The boot.dev solution assumes all items are on the same level with no leading whitespace. The same goes for ordered lists
            node = ParentNode("ul", [])
            for l in block.splitlines():
                l = l.strip()
                node.children.append(ParentNode("li", text_to_htmlnodes(l[1:])))
            return node
        case "ordered_list":
            node = ParentNode("ol", [], None)
            for l in block.splitlines():
                l = l.strip()
                node.children.append(ParentNode("li", text_to_htmlnodes(l[3:])))
            return node
        case "paragraph":
            return ParentNode("p", text_to_htmlnodes(block))


def text_to_htmlnodes(text):
    res = []
    for node in text_to_textnodes(text):
        res.append(node.to_html_node())
    return res


# Assumes that leading and trailing whitespace has been stripped
def block_type(block):
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
            if len(s) < 2 or s[0:3] != f"{current_line}. ":
                ordered_list = False
                break
            current_line += 1
        if ordered_list:
            return "ordered_list"

    return "paragraph"


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
