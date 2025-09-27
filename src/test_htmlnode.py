import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()
