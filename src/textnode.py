#!/usr/bin/env python3
from htmlnode import LeafNode


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
