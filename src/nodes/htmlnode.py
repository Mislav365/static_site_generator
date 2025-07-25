class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("not properly implemented")

    def props_to_html(self):
        props = ""
        for elem in self.props:
            props += f'{elem}="{self.props[elem]}" '
        return props.rstrip()

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

