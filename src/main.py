#!/usr/bin/env python3

from textnode import TextNode
from htmlnode import HTMLNode


def main():
    t = TextNode("text", "type", "example.com")
    print(t)
    node = HTMLNode("a", "example.com", None, {"href": "boot.dev", "target": "_blank"})
    print(node.props_to_html())
    print(node)


if __name__ == "__main__":
    main()
