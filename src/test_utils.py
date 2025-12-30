import unittest

from utils import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextType, TextNode


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev", "alt": "This is an image node"})

    def test_invalid_text_type(self):
        node = TextNode("This is an invalid node", "invalid")
        self.assertRaises(ValueError, text_node_to_html_node, node)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold(self):
        nodes = [TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("bolded phrase", TextType.BOLD), TextNode(" in the middle", TextType.TEXT)])

    def test_two_bold(self):
        nodes = [TextNode("This is text with a **bolded phrase** and another **bolded phrase** in the middle", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("bolded phrase", TextType.BOLD), TextNode(" and another ", TextType.TEXT), TextNode("bolded phrase", TextType.BOLD), TextNode(" in the middle", TextType.TEXT)])

    def test_italic(self):
        nodes = [TextNode("This is text with a _italicized phrase_ in the middle", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("italicized phrase", TextType.ITALIC), TextNode(" in the middle", TextType.TEXT)])

    def test_code(self):
        nodes = [TextNode("This is text with a `code` in the middle", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" in the middle", TextType.TEXT)])

    def test_non_text_node(self):
        nodes = [TextNode("This is text with a **bolded phrase** in the middle", TextType.BOLD)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, nodes)

    def test_invalid_syntax(self):
        nodes = [TextNode("This is text with a **bolded phrase in the middle", TextType.TEXT)]
        self.assertRaises(ValueError, split_nodes_delimiter, nodes, "**", TextType.BOLD)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])


if __name__ == "__main__":
    unittest.main()