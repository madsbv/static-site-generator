#!/usr/bin/env python3
import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test(self):
        node = HTMLNode(
            "a", "example.com", None, {"href": "boot.dev", "target": "_blank"}
        )
        self.assertEqual(node.props_to_html(), ' href="boot.dev" target="_blank"')


from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test(self):
        node = LeafNode("example.com", "a", {"href": "boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="boot.dev" target="_blank"')

    def test_to_html(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node1.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(
            node2.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )


from htmlnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_boot_dev(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_nested_nodes(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        nesting_node = ParentNode("a", [node, LeafNode("h1", "header")])
        self.assertEqual(
            nesting_node.to_html(),
            "<a><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><h1>header</h1></a>",
        )


if __name__ == "__main__":
    unittest.main()
