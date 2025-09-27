import unittest

from textnode import TextNode, TextType
from markdown_parsing import split_nodes_delimiter


class TestMarkdownParsing(unittest.TestCase):
    def test_split_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.PLAIN),
            ],
        )

    def test_split_nodes_bold_italic(self):
        node = TextNode(
            "This is text with a **bold** word and an _italic_ word", TextType.PLAIN
        )
        new_nodes_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes_italic = split_nodes_delimiter(new_nodes_bold, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes_bold,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" word and an _italic_ word", TextType.PLAIN),
            ],
        )
        self.assertEqual(
            new_nodes_italic,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" word and an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.PLAIN),
            ],
        )

    def test_split_nodes_multi_word_bold_italic_beginning_end(self):
        node = TextNode(
            "**This is bold text** and maybe there's also something _italic at the end_",
            TextType.PLAIN,
        )
        new_nodes_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes_italic = split_nodes_delimiter(new_nodes_bold, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes_bold,
            [
                TextNode("This is bold text", TextType.BOLD),
                TextNode(
                    " and maybe there's also something _italic at the end_",
                    TextType.PLAIN,
                ),
            ],
        )
        self.assertEqual(
            new_nodes_italic,
            [
                TextNode("This is bold text", TextType.BOLD),
                TextNode(" and maybe there's also something ", TextType.PLAIN),
                TextNode("italic at the end", TextType.ITALIC),
            ],
        )


if __name__ == "__main__":
    unittest.main()
