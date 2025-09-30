import unittest

from generate_page import extract_title


class TestGeneratePage(unittest.TestCase):
    def test_extract_title_simple(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_top(self):
        markdown = """
        # My todo-list

        This is a little markdown paragraph that extends this markdown file a little

        ## bucket list
        - buy some clothes
        - do the dishes
        - prepare food
        """
        self.assertEqual(extract_title(markdown), "My todo-list")

    def test_extract_title_not_top(self):
        markdown = """
        This is a little markdown paragraph that extends this markdown file a little

        # My todo-list

        ## bucket list
        - buy some clothes
        - do the dishes
        - prepare food
        """
        self.assertEqual(extract_title(markdown), "My todo-list")

    def test_extract_title_two_h1s(self):
        markdown = """
        # My little markdown file
        This is a little markdown paragraph that extends this markdown file a little

        # My todo-list

        ## bucket list
        - buy some clothes
        - do the dishes
        - prepare food
        """
        self.assertEqual(extract_title(markdown), "My little markdown file")

    def test_extract_title_no_h1(self):
        markdown = """
        ## My little markdown file
        This is a little markdown paragraph that extends this markdown file a little

        ## My todo-list

        ### bucket list
        - buy some clothes
        - do the dishes
        - prepare food
        """
        self.assertRaises(Exception, extract_title, markdown)
