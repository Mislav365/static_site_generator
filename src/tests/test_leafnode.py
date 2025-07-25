import unittest

from nodes.leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_LeafNode_to_html_value_None(self):
        node = LeafNode(value = None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_LeafNode_to_html_only_value_set(self):
        node = LeafNode(value = "This is a value")
        self.assertEqual(node.to_html(), "This is a value")

    def test_LeafNode_to_html_no_params(self):
        node = LeafNode(value = "This is a value", tag="p")
        self.assertEqual(node.to_html(), "<p>This is a value</p>")

    def test_LeafNode_to_html_all_set(self):
        node = LeafNode(value = "This is a value", tag="a",props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">This is a value</a>')

if __name__ == "__main__":
    unittest.main()