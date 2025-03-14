from textnode  import TextNode, TextType
from htmlnode import *


def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node)

def text_node_to_html_node(text_node):
        match text_node:
            case TextType.TEXT:
                return LeafNode(None, text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.CODE:
                return LeafNode("code", text_node.text)
            case TextType.LINK:
                return LeafNode("a", text_node.text, text_node.url)
            case TextType.IMAGE:
                return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
main() 