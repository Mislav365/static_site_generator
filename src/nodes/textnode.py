from enum import Enum

from nodes.leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case(TextType.TEXT):
            return LeafNode(value = text_node.text)
        case(TextType.BOLD):
            return LeafNode(value = text_node.text, tag= "b")
        case(TextType.ITALIC):
            return LeafNode(value = text_node.text, tag= "i")
        case(TextType.CODE):
            return LeafNode(value = text_node.text, tag= "code")
        case(TextType.LINK):
            return LeafNode(value = text_node.text, tag= "a", props={"href": text_node.url})
        case(TextType.IMAGE):
            return LeafNode(value = "", tag= "img", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Excepction("invalid text type")
