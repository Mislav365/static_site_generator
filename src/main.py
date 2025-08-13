from nodes.textnode import TextNode,TextType
from markdownparser import markdown_to_html_node

def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node)
    markdown = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """
    node = markdown_to_html_node(markdown)
    print(node.to_html())


if __name__ == "__main__":
    main()