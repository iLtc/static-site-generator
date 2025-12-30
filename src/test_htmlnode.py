import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_two_children(self):
        child_node_1 = LeafNode("span", "child 1")
        child_node_2 = LeafNode("span", "child 2")
        parent_node = ParentNode("div", [child_node_1, child_node_2])
        self.assertEqual(parent_node.to_html(), "<div><span>child 1</span><span>child 2</span></div>")

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child", props={"class": "child-class"})
        parent_node = ParentNode("div", [child_node], props={"class": "container", "id": "main"})
        self.assertEqual(parent_node.to_html(), "<div class=\"container\" id=\"main\"><span class=\"child-class\">child</span></div>")

    def test_to_html_no_tag(self):
        parent_node = ParentNode(None, [LeafNode("span", "child")])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertRaises(ValueError, parent_node.to_html)


if __name__ == "__main__":
    unittest.main()