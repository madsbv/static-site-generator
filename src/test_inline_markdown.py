#!/usr/bin/env python3

import unittest

from textnode import TextNode
from inline_markdown import (
    split_nodes_images,
    split_nodes_links,
    split_nodes_delimiter,
    text_to_textnodes,
    extract_markdown_images,
    extract_markdown_links,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes(self):
        text = "Text with *italic* and **bold**"
        text_node = TextNode(text, "text")
        test_cases = [
            (
                [text_node],
                [
                    TextNode("Text with ", "text"),
                    TextNode("italic", "italic"),
                    TextNode(" and **bold**", "text"),
                ],
                "*",
                "italic",
            ),
            (
                [text_node],
                [
                    TextNode("Text with *italic* and ", "text"),
                    TextNode("bold", "bold"),
                ],
                "**",
                "bold",
            ),
        ]

        for input, ex, delim, type in test_cases:
            self.assertEqual(split_nodes_delimiter(input, delim, type), ex)

    def test_split_mismatched_nodes(self):
        node = TextNode("*This* **contains** *mismatched delimiters**", "text")
        # These cases should raise errors, so we don't specify expected results
        test_cases = [
            (
                [node],
                "**",
                "bold",
            ),
            (
                [node],
                "*",
                "italic",
            ),
        ]
        for input, delim, type in test_cases:
            failed = False
            try:
                split_nodes_delimiter(input, delim, type)
            except ValueError:
                failed = True
            self.assertEqual(failed, True)

    def test_split_node_starting_with_delimiter(self):
        node = TextNode("`This` starts with delim", "text")
        split_node = split_nodes_delimiter([node], "`", "code")
        expected = [TextNode("This", "code"), TextNode(" starts with delim", "text")]
        self.assertEqual(split_node, expected)

    def test_extract_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        result = extract_markdown_images(text)
        expected = [
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("another", "https://i.imgur.com/dfsdkjfd.png"),
        ]
        self.assertEqual(result, expected)

    def test_extract_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        result = extract_markdown_links(text)
        expected = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]
        self.assertEqual(result, expected)

    def test_extract_links_avoids_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)

    def test_split_nodes_images(self):
        image_node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)",
            "text",
        )
        link_node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
            "text",
        )
        res = split_nodes_images([image_node, link_node])
        expected = [
            TextNode("This is text with an ", "text"),
            TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and ", "text"),
            TextNode("another", "image", "https://i.imgur.com/dfsdkjfd.png"),
            TextNode(
                "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
                "text",
            ),
        ]
        self.assertEqual(res, expected)

    def test_split_nodes_links(self):
        image_node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)",
            "text",
        )
        link_node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
            "text",
        )
        res = split_nodes_links([image_node, link_node])
        expected = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)",
                "text",
            ),
            TextNode(
                "This is text with a ",
                "text",
            ),
            TextNode("link", "link", "https://www.example.com"),
            TextNode(" and ", "text"),
            TextNode("another", "link", "https://www.example.com/another"),
        ]
        self.assertEqual(res, expected)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)


if __name__ == "__main__":
    unittest.main()
