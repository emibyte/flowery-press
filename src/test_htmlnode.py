import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq_props_to_html(self):
        node = HTMLNode(
            "p",
            "this is a value",
            None,
            {"test": "result1", "href": "https://www.example.com", "a": "b"},
        )
        expected = ' test="result1" href="https://www.example.com" a="b"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_none(self):
        node = HTMLNode(
            "p",
            "this is a value",
        )
        self.assertEqual(node.props, None)

    def test_values(self):
        node = HTMLNode(
            "div",
            "some text",
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "some text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_stringify(self):
        node = HTMLNode(
            "p",
            "this is a value",
            [HTMLNode()],
            {"test": "result1", "class": "paragraph-text", "background": "blue"},
        )
        expected = "HTMLNode(tag: p, value: this is a value, children: [HTMLNode(tag: None, value: None, children: None, props: None)], props: {'test': 'result1', 'class': 'paragraph-text', 'background': 'blue'})"
        self.assertEqual(node.__repr__(), expected)

    def test_leaf_to_html_p_no_attribs(self):
        node = LeafNode("p", "Hello world!")
        self.assertEqual(node.to_html(), "<p>Hello world!</p>")

    def test_leaf_to_html_p_with_attribs(self):
        node = LeafNode(
            "p", "Hello world!", {"class": "testimonial", "foreground": "pink"}
        )
        self.assertEqual(
            node.to_html(), '<p class="testimonial" foreground="pink">Hello world!</p>'
        )

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Home", {"href": "index.html"})
        self.assertEqual(node.to_html(), '<a href="index.html">Home</a>')

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "This is some bold text")
        self.assertEqual(node.to_html(), "<b>This is some bold text</b>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Some text")
        self.assertEqual(node.to_html(), node.value)


if __name__ == "__main__":
    unittest.main()
