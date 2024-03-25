#!/usr/bin/env python3
import unittest

from block_markdown import block_type, markdown_to_blocks, markdown_to_html_node
from htmlnode import ParentNode, LeafNode


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
                self.assertEqual(block_type(b), type)

    def test_markdown_to_html_node(self):
        md = """ # A heading

## A subheading

> This is
> a quote

* and
* a
* list

- and
- another

1. Time for an
2. ordered
3. list

```
print("Hello world")
```

And finally, this is just a normal paragraph.
"""
        expected = ParentNode(
            """div""",
            [
                ParentNode("""h1""", [LeafNode(None, """A heading""", None)], None),
                ParentNode("""h2""", [LeafNode(None, """A subheading""", None)], None),
                ParentNode(
                    """blockquote""",
                    [
                        LeafNode(
                            None,
                            """ This is
 a quote
""",
                            None,
                        )
                    ],
                    None,
                ),
                ParentNode(
                    """ul""",
                    [
                        ParentNode("""li""", [LeafNode(None, """ and""", None)], None),
                        ParentNode("""li""", [LeafNode(None, """ a""", None)], None),
                        ParentNode("""li""", [LeafNode(None, """ list""", None)], None),
                    ],
                    None,
                ),
                ParentNode(
                    """ul""",
                    [
                        ParentNode("""li""", [LeafNode(None, """ and""", None)], None),
                        ParentNode(
                            """li""", [LeafNode(None, """ another""", None)], None
                        ),
                    ],
                    None,
                ),
                ParentNode(
                    """ol""",
                    [
                        ParentNode(
                            """li""",
                            [LeafNode(None, """Time for an""", None)],
                            None,
                        ),
                        ParentNode(
                            """li""", [LeafNode(None, """ordered""", None)], None
                        ),
                        ParentNode("""li""", [LeafNode(None, """list""", None)], None),
                    ],
                    None,
                ),
                LeafNode(
                    """pre""",
                    """
print("Hello world")
""",
                    None,
                ),
                ParentNode(
                    """p""",
                    [
                        LeafNode(
                            None,
                            """And finally, this is just a normal paragraph.""",
                            None,
                        )
                    ],
                    None,
                ),
            ],
            None,
        )

        # Correctness of "expected" verified by hand, and by outputting HTML and rendering in browser to check that we get the expected output.
        self.assertEqual(markdown_to_html_node(md), expected)


if __name__ == "__main__":
    unittest.main()
