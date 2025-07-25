from nodes.textnode import TextType

DELIMITERS = {
    "**": TextType.BOLD,
    "_": TextType.ITALIC,
    "`": TextType.CODE,
}