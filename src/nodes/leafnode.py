from nodes.htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        else:
            string_to_html = f"<{self.tag}"
            if self.props:
                string_to_html += f" {self.props_to_html()}"
            string_to_html += f">{self.value}</{self.tag}>"
            return string_to_html
