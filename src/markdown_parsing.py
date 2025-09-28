import re

from textnode import TextNode, TextType


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
