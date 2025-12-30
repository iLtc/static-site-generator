import re

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)

        case TextType.BOLD:
            return LeafNode("b", text_node.text)

        case TextType.ITALIC:
            return LeafNode("i", text_node.text)

        case TextType.CODE:
            return LeafNode("code", text_node.text)

        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})

        case TextType.IMAGE:
            return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})

        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text

        if delimiter not in text:
            new_nodes.append(node)
            continue

        if text.count(delimiter) % 2 != 0:
            raise ValueError(f"Invalid Markdown syntax")

        while delimiter in text:
            before, middle, after = text.split(delimiter, 2)

            new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(middle, text_type))
            text = after

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text: str) -> list[str]:
    return re.findall(r"!\[(.+?)\]\((.+?)\)", text)

def extract_markdown_links(text: str) -> list[str]:
    return re.findall(r"\[(.+?)\]\((.+?)\)", text)
