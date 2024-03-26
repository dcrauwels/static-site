import unittest

from htmlnode import HTMLNode, LeafNode

class TestTextNode(unittest.TestCase):
    def test_repr(self):
        node1 = HTMLNode("a", "Link", None, {"href": "www.google.com"})
        node2 = HTMLNode("p", "Paragraph")
        print(node1)
        print(node2)

    def test_props_to_html(self):
        node1 = HTMLNode("a", "Link", None, {"href": "www.google.com"})
        print(node1.props_to_html())

    def test_leafnode(self):
        node1 = LeafNode("a", "Link", {"href": "www.google.com"})
        print(node1.to_html())

if __name__ == "__main__":
    unittest.main()

