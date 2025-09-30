import re

from enum import Enum
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


# NOTE: move the block stuff into its own file
#       also same for the tests
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            raw_text = " ".join(block.split("\n"))
            text_nodes = text_to_textnodes(raw_text)
            child_html_nodes = list(map(text_node_to_html_node, text_nodes))
            return ParentNode("p", child_html_nodes)
        case BlockType.HEADING:
            level, text = get_heading_data(block)
            text_nodes = text_to_textnodes(text)
            child_html_nodes = list(map(text_node_to_html_node, text_nodes))
            return ParentNode(f"h{level}", child_html_nodes)
        case BlockType.CODE:
            node = TextNode(block[4:-3], TextType.PLAIN)
            child_html_node = text_node_to_html_node(node)
            return ParentNode("pre", [ParentNode("code", [child_html_node])])
        case BlockType.QUOTE:
            raw_text = get_quote_text(block)
            text_nodes = text_to_textnodes(raw_text)
            child_html_nodes = list(map(text_node_to_html_node, text_nodes))
            return ParentNode("blockquote", child_html_nodes)
        case BlockType.UNORDERED_LIST:
            return parse_unordered_list(block)
        case BlockType.ORDERED_LIST:
            return parse_ordered_list(block)
        case _:
            raise ValueError(f'not supported block type: "{block_type}"')


def get_heading_data(block: str) -> tuple[int, str]:
    level = 0
    for char in block[:7]:
        if char == "#":
            level += 1
        else:
            break
    return level, block[level + 1 :]


def get_quote_text(block: str) -> str:
    lines = block.split("\n")
    pruned_lines = []
    for line in lines:
        pruned_lines.append(line.lstrip(">").strip())
    return " ".join(pruned_lines)


def parse_unordered_list(block: str) -> ParentNode:
    lines = block.split("\n")
    list_items = []
    for line in lines:
        if not line.strip():
            continue
        item = line[2:]
        text_nodes = text_to_textnodes(item)
        html_child_nodes = list(map(text_node_to_html_node, text_nodes))
        list_items.append(ParentNode("li", html_child_nodes))
    return ParentNode("ul", list_items)


def parse_ordered_list(block: str) -> ParentNode:
    lines = block.split("\n")
    list_items = []
    for line in lines:
        if not line.strip():
            continue
        item = line[3:]
        text_nodes = text_to_textnodes(item)
        html_child_nodes = list(map(text_node_to_html_node, text_nodes))
        list_items.append(ParentNode("li", html_child_nodes))
    return ParentNode("ol", list_items)


def block_to_block_type(block: str) -> BlockType:
    # NOTE: change this to a simpler check that doesnt (mis)use a regexp
    pattern = re.compile(r"^(#{1,6})\s")
    if bool(pattern.match(block)):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    quote = True
    unordered_list = True
    for line in lines:
        if not line.startswith(">"):
            quote = False
        if not line.startswith("- "):
            unordered_list = False
    if quote:
        return BlockType.QUOTE
    elif unordered_list:
        return BlockType.UNORDERED_LIST

    ordered_list = False
    count = 1
    if block.startswith("1. "):
        ordered_list = True
        for line in lines:
            if not line.startswith(f"{count}. "):
                ordered_list = False
                break
            count += 1
    if ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    return list(
        filter(
            lambda line: len(line) > 0, map(lambda s: s.strip(), markdown.split("\n\n"))
        )
    )


def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text, TextType.PLAIN)
    nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        # NOTE: there needs to be an even amount of the delimiter for it to be valid markdown
        #       which means the length of the splitted list has to be odd
        if len(parts) % 2 == 0:
            raise ValueError(
                "invalid markdown: there needs to be an even amount of delimiters."
            )
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], node.text_type))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    # NOTE: markdown image => !["alt-text"]("uri")
    regex = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(regex, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    # NOTE: markdown image => ["alt-text"]("uri")
    #       (?<!x) is negative lookbehind to make sure we dont match on images and treat them as links
    regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(regex, text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        text_left = node.text
        for alt_text, url in matches:
            image = f"![{alt_text}]({url})"
            head, rest = text_left.split(image, maxsplit=1)
            if head:
                new_nodes.append(TextNode(head, TextType.PLAIN))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            text_left = rest
        if len(text_left) > 0:
            new_nodes.append(TextNode(text_left, TextType.PLAIN))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        text_left = node.text
        for text, url in matches:
            link = f"[{text}]({url})"
            head, rest = text_left.split(link, maxsplit=1)
            if head:
                new_nodes.append(TextNode(head, TextType.PLAIN))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            text_left = rest
        if len(text_left) > 0:
            new_nodes.append(TextNode(text_left, TextType.PLAIN))
    return new_nodes
