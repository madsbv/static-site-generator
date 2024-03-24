#!/usr/bin/env python3
import unittest

from block_markdown import markdown_to_blocks


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = r"""This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
   This is the same paragraph on a new line

* This is a list
* with items"""
        expected = [
            "This is **bolded** paragraph",
            """This is another paragraph with *italic* text and `code` here
   This is the same paragraph on a new line""",
            r"""* This is a list
* with items""",
        ]
        self.assertEqual(markdown_to_blocks(text), expected)


if __name__ == "__main__":
    unittest.main()
