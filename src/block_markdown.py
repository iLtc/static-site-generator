from enum import Enum
import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    results = []

    for line in markdown.split("\n\n"):
        line = line.strip()

        if not line:
            continue

        results.append(line)

    return results

def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} .+$", block):
        return BlockType.HEADING

    if re.match(r"^```.+?```$", block, re.DOTALL):
        return BlockType.CODE

    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(re.match(r"^\d+\. .+$", line) for line in lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text: str) -> list[HTMLNode]:
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]

def heading_to_html_node(heading: str) -> HTMLNode:
    heading, text = heading.split(" ", 1)
    level = len(heading)

    return ParentNode("h" + str(level), text_to_children(text))

def code_to_html_node(code: str) -> HTMLNode:
    code = code.replace("```", "").strip()

    leaf_node = LeafNode("code", code)
    parent_node = ParentNode("pre", [leaf_node])

    return parent_node

def quote_to_html_node(quote: str) -> HTMLNode:
    lines = []

    for line in quote.split("\n"):
        lines.append(line.replace("> ", ""))

    return ParentNode("blockquote", text_to_children(" ".join(lines)))

def unordered_list_to_html_node(unordered_list: str) -> HTMLNode:
    children = []

    for line in unordered_list.split("\n"):
        children.append(ParentNode("li", text_to_children(line.replace("- ", ""))))

    return ParentNode("ul", children)

def ordered_list_to_html_node(ordered_list: str) -> HTMLNode:
    children = []

    for line in ordered_list.split("\n"):
        children.append(ParentNode("li", text_to_children(line.split(".", 1)[1].strip())))

    return ParentNode("ol", children)

def paragraph_to_html_node(paragraph: str) -> HTMLNode:
    paragraph = paragraph.replace("\n", " ")

    return ParentNode("p", text_to_children(paragraph))

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.HEADING:
                children.append(heading_to_html_node(block))
            case BlockType.CODE:
                children.append(code_to_html_node(block))
            case BlockType.QUOTE:
                children.append(quote_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                children.append(unordered_list_to_html_node(block))
            case BlockType.ORDERED_LIST:
                children.append(ordered_list_to_html_node(block))
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_html_node(block))

    return ParentNode("div", children)
