import unittest

from textnode import TextNode, TextType
from markdown_parsing import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


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

    def test_extracting_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extracting_links(self):
        text = "This is text with a link [to google](https://www.google.com) and [to youtube](https://www.youtube.com)"
        self.assertListEqual(
            extract_markdown_links(text),
            [
                ("to google", "https://www.google.com"),
                ("to youtube", "https://www.youtube.com"),
            ],
        )

    def test_extracting_links_when_images_also_present(self):
        text = "This is text containing a link [to google](https://www.google.com) and an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and another link [to youtube](https://www.youtube.com) and another image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            extract_markdown_links(text),
            [
                ("to google", "https://www.google.com"),
                ("to youtube", "https://www.youtube.com"),
            ],
        )

    def test_extracting_images_when_links_also_present(self):
        text = "This is text containing a link [to google](https://www.google.com) and an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and another link [to youtube](https://www.youtube.com) and another image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
