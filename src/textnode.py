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

    def to_html_node(self):
        tags_dict = {
            "text": None,
            "bold": "b",
            "italic": "i",
            "code": "code",
            "link": "a",
            "image": "img",
        }
        if self.text_type not in tags_dict.keys():
            raise Exception(f"Invalid text type '{self.text_type}' in text node {self}")

        tag = tags_dict[self.text_type]

        props = None
        value = self.text
        if tag == "a":
            props = {"href": self.url}

        if tag == "img":
            props = {"src": self.url, "alt": self.text}
            value = ""
        return LeafNode(tag, value, props)
