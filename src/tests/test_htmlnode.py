import unittest

from nodes.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_empty_HTMLNode(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_HTMLNode_props_to_html(self):
        node = HTMLNode(props = {"alpha":"romeo", "target":25})
        expected_string = 'alpha="romeo" target="25"'
        self.assertEqual(node.props_to_html(), expected_string)

    def test_HTMLNode_print(self):
        node = HTMLNode(value = 25)
        expected_string = "HTMLNode(None, 25, None, None)"
        self.assertEqual(str(node), expected_string)

if __name__ == "__main__":
    unittest.main()