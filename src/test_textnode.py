import unittest

from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node1, node2)

    def test_text_to_leaf(self):
        node1 = TextNode("Body", "image", "https://www.google.com")
        lnode1 = text_node_to_html_node(node1)
        node2 = LeafNode("img", "", {"src": "https://www.google.com", "alt": "Body"})
        self.assertEqual(lnode1.to_html(),node2.to_html())

if __name__ == "__main__":
    unittest.main()
