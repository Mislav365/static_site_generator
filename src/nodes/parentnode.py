from nodes.htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag,children, props=None):
        super().__init__(tag,None,children,props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag.")
        if self.children is None:
            raise ValueError("All parent nodes must have children defined.")
        else:
            string_to_html = f"<{self.tag}>"
            for child in self.children:
                string_to_html += child.to_html()
            string_to_html += f"</{self.tag}>"
            return string_to_html