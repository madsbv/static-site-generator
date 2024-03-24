#!/usr/bin/env python3
import unittest
import pdb

from textnode import TextNode, text_node_to_html_node, split_nodes_delimiter
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")

        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", "bold", "example.com")
        node2 = TextNode("This is a text node", "bold", "example.com")
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This i a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a text node", "bod")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a text node", "bold", "example.com")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_neq_url_some(self):
        node = TextNode("This is a text node", "bold", "example.com")
        node2 = TextNode("This is a text node", "bold", "asdf.com")
        self.assertNotEqual(node, node2)

    def test_to_html_node(self):
        test_cases = [
            (TextNode("Text node", "text"), LeafNode(None, "Text node")),
            (TextNode("Bold node", "bold"), LeafNode("b", "Bold node")),
            (TextNode("Italic node", "italic"), LeafNode("i", "Italic node")),
            (TextNode("Code node", "code"), LeafNode("code", "Code node")),
            (
                TextNode("Link node", "link", "example.com"),
                LeafNode("a", "Link node", {"href": "example.com"}),
            ),
            (
                TextNode("Image node", "image", "image.png"),
                LeafNode("img", "", {"src": "image.png", "alt": "Image node"}),
            ),
        ]
        for text_node, expected_html_node in test_cases:
            converted_node = text_node_to_html_node(text_node)
            self.assertEqual(expected_html_node, converted_node)

    def test_invalid_to_html_node(self):
        invalid_conversion = TextNode("Invalid node", "not a html tag")
        entered_except = False
        try:
            text_node_to_html_node(invalid_conversion)
        except:
            entered_except = True
        self.assertEqual(entered_except, True)

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
            print(input)
            print(failed)
            self.assertEqual(failed, True)

    def test_split_node_starting_with_delimiter(self):
        node = TextNode("`This` starts with delim", "text")
        split_node = split_nodes_delimiter([node], "`", "code")
        expected = [TextNode("This", "code"), TextNode(" starts with delim", "text")]
        self.assertEqual(split_node, expected)

    # TODO: Write more tests, particularly in the nested case, for mismatched delims, maybe for text that starts with delims


if __name__ == "__main__":
    unittest.main()
