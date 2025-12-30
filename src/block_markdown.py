from enum import Enum
import re


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
