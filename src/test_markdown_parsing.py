import unittest

from src.htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType
from markdown_parsing import (
    block_to_block_type,
    BlockType,
    markdown_to_blocks,
    markdown_to_html_node,
    parse_unordered_list,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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

    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_images_same_one_twice(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and the same ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and the same ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.example.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_links_link_at_start(self):
        node = TextNode(
            "[link](https://www.google.com) and another [second link](https://www.example.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://www.example.com)"
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ],
        )

    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_block(self):
        markdown = """
This is **bolded** paragraph



- This is a list
- with items
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        self.assertEqual(
            block_to_block_type("This is a **bolded** paragraph"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("- This is a list\n- oh look, another item"),
            BlockType.UNORDERED_LIST,
        )
        self.assertEqual(
            block_to_block_type("1. This is a list\n2. oh look, another item"),
            BlockType.ORDERED_LIST,
        )
        self.assertNotEqual(
            block_to_block_type(
                "1. This is a list\n2 .oh look, another item\n4. not a ordered list anymore"
            ),
            BlockType.ORDERED_LIST,
        )
        self.assertEqual(
            block_to_block_type(
                "```\nlet x = 1\nlet y = ref 0\n(* ocaml is kinda cool *)\n```"
            ),
            BlockType.CODE,
        )
        self.assertEqual(
            block_to_block_type(
                "> this is a quote\n> that has multiple lines\n> which are all part of a single quoute block"
            ),
            BlockType.QUOTE,
        )
        self.assertEqual(
            block_to_block_type("# h1"),
            BlockType.HEADING,
        )
        self.assertEqual(
            block_to_block_type("#### h4"),
            BlockType.HEADING,
        )
        self.assertEqual(
            block_to_block_type("###### h6"),
            BlockType.HEADING,
        )
        self.assertNotEqual(
            block_to_block_type("####### h7 (doesnt exist)"),
            BlockType.HEADING,
        )

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_list_html_nodes(self):
        markdown = """
- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)
"""
        self.assertEqual(
            parse_unordered_list(markdown),
            ParentNode(
                "ul",
                [
                    ParentNode(
                        "li",
                        [
                            LeafNode(
                                "a",
                                "Why Glorfindel is More Impressive than Legolas",
                                {"href": "/blog/glorfindel"},
                            )
                        ],
                    ),
                    ParentNode(
                        "li",
                        [
                            LeafNode(
                                "a",
                                "Why Tom Bombadil Was a Mistake",
                                {"href": "/blog/tom"},
                            )
                        ],
                    ),
                    ParentNode(
                        "li",
                        [
                            LeafNode(
                                "a",
                                'The Unparalleled Majesty of "The Lord of the Rings"',
                                {"href": "/blog/majesty"},
                            )
                        ],
                    ),
                ],
            ),
        )


if __name__ == "__main__":
    unittest.main()
