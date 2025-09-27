from textnode import TextNode, TextType


def main():
    node = TextNode("some anchor text", TextType.LINK, "https://www.example.com")
    print(node)


main()
