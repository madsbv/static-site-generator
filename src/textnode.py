#!/usr/bin/env python3
from htmlnode import LeafNode
from src.extract import extract_markdown_images, extract_markdown_links


class TextNode:
    def __init__(self, text, text_type=None, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    tags_dict = {
        "text": None,
        "bold": "b",
        "italic": "i",
        "code": "code",
        "link": "a",
        "image": "img",
    }
    if text_node.text_type not in tags_dict.keys():
        raise Exception(
            f"Invalid text type '{text_node.text_type}' in text node {text_node}"
        )

    tag = tags_dict[text_node.text_type]

    props = None
    value = text_node.text
    if tag == "a":
        props = {"href": text_node.url}
    if tag == "img":
        props = {"src": text_node.url, "alt": text_node.text}
        value = ""
    return LeafNode(tag, value, props)


def split_nodes_links(nodes):
    res = []
    for n in nodes:
        if n.text_type != "text":
            res.append(n)
            continue
        images = extract_markdown_links(n.text)
        if len(images) == 0:
            res.append(n)
            continue
        remaining = n.text
        for desc, link in images:
            before, remaining = remaining.split(f"[{desc}]({link})")
            res.append(TextNode(before, "text"))
            res.append(TextNode(desc, "link", link))
        if len(remaining) != 0:
            res.append(TextNode(remaining, "text"))
    return res


def split_nodes_images(nodes):
    res = []
    for n in nodes:
        if n.text_type != "text":
            res.append(n)
            continue
        images = extract_markdown_images(n.text)
        if len(images) == 0:
            res.append(n)
            continue
        remaining = n.text
        for desc, link in images:
            before, remaining = remaining.split(f"![{desc}]({link})")
            res.append(TextNode(before, "text"))
            res.append(TextNode(desc, "image", link))
        if len(remaining) != 0:
            res.append(TextNode(remaining, "text"))
    return res


# NOTE: If the delimiters are mismatched, raises `ValueError`.
def split_nodes_delimiter(nodes, delimiter, text_type):
    res = []
    for n in nodes:
        try:
            res.extend(split_node(n, delimiter, text_type))
        except ValueError as e:
            raise e
    return res


# If `node` is a text node, split its text using `delimiter` as both opening and closing delimiter, and assigning `text_type` to text enclosed by `delimiter`.
# NOTE: If the delimiters are mismatched, raises `ValueError`.
# NOTE: If `delimiter` occurs twice in a row, this skips over both occurences, preserving them in the text. This is mainly to handle  `*` vs `**` in markdown for italics vs bold; if we didn't do this, bold tags would just get deleted completely from the text.
def split_node(node, delimiter, text_type):
    if node.text_type != "text":
        return [node]

    l = len(delimiter)
    i = 0
    prev_delim = -l
    parts = []
    while i < len(node.text):
        next = node.text.find(delimiter, i)
        if next == -1:
            # there's no more delimiters left in the string
            break
        # NOTE: If we want to special case `*` vs `**`, we can add a check for `delimiter == "*"` here.
        if node.text[next + l : next + 2 * l] == delimiter:
            i = next + 2 * l
        else:
            parts.append(node.text[prev_delim + l : next])
            prev_delim = next
            i = next + l
    parts.append(node.text[prev_delim + l :])

    if len(parts) % 2 == 0:
        raise ValueError(
            f"Missing closing delimiter {delimiter} in string '{node.text}', found parts:\n{parts}"
        )
    res = []
    for i in range(len(parts)):
        # Text parts and delimited parts alternate starting with a text part (which might be empty)
        # We might as well throw away empty parts
        if len(parts[i]) == 0:
            continue
        if i % 2 == 0:
            res.append(TextNode(parts[i], "text"))
        else:
            res.append(TextNode(parts[i], text_type))
    return res
