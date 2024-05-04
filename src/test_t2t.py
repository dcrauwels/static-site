import unittest

from textnode import TextNode, text_node_to_html_node, split_nodes_delimiter, text_to_textnodes
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_text_to_textnodes_mixed(self):
        text1 = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        snode1 = text_to_textnodes(text1)
        rnode1 = [
                TextNode("This is ", "text"),
                TextNode("text", "bold"),
                TextNode(" with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word and a ", "text"),
                TextNode("code block", "code"),
                TextNode(" and an ", "text"),
                TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", "text"),
                TextNode("link", "link", "https://boot.dev"),
                ]
        self.assertEqual(snode1, rnode1)

if __name__ == "__main__":
    unittest.main()
