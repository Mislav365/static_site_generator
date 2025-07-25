import unittest

from nodes.leafnode import LeafNode
from nodes.parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_ParentNode_to_html_tag_None(self):
        node = ParentNode(tag = None, children = [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_ParentNode_to_html_children_None(self):
        node = ParentNode(tag = 25, children = None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_ParentNode_to_html_children_empty(self):
        node = ParentNode(tag = 'p', children = [])
        self.assertEqual(node.to_html(), f"<p></p>")

    def test_parent_node_to_html_with_children(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_node_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()