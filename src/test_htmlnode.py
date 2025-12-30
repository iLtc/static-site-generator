import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("div", "Hello, world!")
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode("div", "Hello, world!", props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), " class=\"container\" id=\"main\"")

    def test_props_to_html_none(self):
        node = HTMLNode("div", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("div", "Hello, world!", props={"class": "container", "id": "main"})
        self.assertEqual(repr(node), "HTMLNode(div, Hello, world!, None, {'class': 'container', 'id': 'main'})")


if __name__ == "__main__":
    unittest.main()