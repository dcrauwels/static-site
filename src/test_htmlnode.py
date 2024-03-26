import unittest

from textnode import TextNode 
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_repr(self):
        node1 = HTMLNode("a", "Link", None, {"href": "www.google.com"})
        node2 = HTMLNode("p", "Paragraph")

    def test_props_to_html(self):
        node1 = HTMLNode("a", "Link", None, {"href": "www.google.com"})

    def test_leafnode(self):
        node1 = LeafNode("a", "Link", {"href": "www.google.com"})
        self.assertEqual(node1.to_html(), "<a href=\"www.google.com\">Link</a>")

    def test_parentnode(self):
        node1 = ParentNode("div", [LeafNode("a", "Link", {"href": "www.google.com"}), LeafNode("a", "Link", {"href": "www.google.com"})])
        self.assertEqual(node1.to_html(), "<div><a href=\"www.google.com\">Link</a><a href=\"www.google.com\">Link</a></div>")
        node2 = ParentNode("p", [node1])

    def test_text_to_leaf(self):
        node1 = TextNode("Body", "image", "https://www.google.com")
        lnode1 = text_node_to_html_node(node1)
        node2 = LeafNode("img", "", {"src": "https://www.google.com", "alt": "Body"})
        self.assertEqual(lnode1.to_html(),node2.to_html())


if __name__ == "__main__":
    unittest.main()

