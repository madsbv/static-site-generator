#!/usr/bin/env python3
import unittest

from textnode import (
    TextNode,
    text_node_to_html_node,
)
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


if __name__ == "__main__":
    unittest.main()
