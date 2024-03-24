#!/usr/bin/env python3
import unittest

from block_markdown import block_to_block_type, markdown_to_blocks


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

    def test_block_to_block_type(self):
        # NOTE: Python string literals with triple quotes handles whitespace in terrible ways, and given that we're partly testing whitespace parsing here, even using something like textwrap.dedent or inspect.cleandoc makes testing hard.
        test_cases = [
            (
                "heading",
                [
                    "# avew",
                    "### aipvo",
                    "###### pivf",
                ],
            ),
            (
                "code",
                ["``` asodiefj ```" "```\nsome code\n```"],
            ),
            (
                "quote",
                [
                    "> simple quote",
                    "> multiline\n> quote",
                    "> multiline\n> quote\n>with\n>weird>\n>spacing",
                ],
            ),
            (
                "unordered_list",
                [
                    "* simple list",
                    "* multiline\n* list",
                    "- multi\n* mixed\n*sdf\n*lasdf*",
                    "* multiline\n* list\n- with\n- multiple\n* levels",
                ],
            ),
            (
                "ordered_list",
                [
                    "1. simple",
                    "1. simple\n2. list",
                ],
            ),
            (
                "paragraph",
                [
                    "asldifj",
                    " # Space before hashtag",
                    "#headingsshouldhavespaces",
                    "####### Too many hashtags",
                    "> Problematic\nquote",
                    "1. Attempt\n2. at\n1. ordered\n2. sublist",
                    "1. out\n3. of order\n2. list",
                    "`` not code ``",
                    "Also not ```code```",
                ],
            ),
        ]
        for type, cases in test_cases:
            for b in cases:
                print(b)
                self.assertEqual(block_to_block_type(b), type)


if __name__ == "__main__":
    unittest.main()
