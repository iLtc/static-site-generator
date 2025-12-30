import unittest

from htmlnode import HTMLNode, LeafNode


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


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_props(self):
        node = LeafNode("p", "Hello, world!", props={"class": "container", "id": "main"})
        self.assertEqual(node.to_html(), "<p class=\"container\" id=\"main\">Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_repr(self):
        node = LeafNode("p", "Hello, world!", props={"class": "container", "id": "main"})
        self.assertEqual(repr(node), "LeafNode(p, Hello, world!, {'class': 'container', 'id': 'main'})")


if __name__ == "__main__":
    unittest.main()