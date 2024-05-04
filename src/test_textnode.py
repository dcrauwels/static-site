import unittest

from textnode import TextNode, text_node_to_html_node, split_nodes_delimiter, text_to_textnodes
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
    
    def test_split_nodes_delimiter(self):
        #Basic **bold** test case for split_nodes_delimiter().
        node1 = TextNode("Greetings **Bold** Text!", "text")
        snode1 = split_nodes_delimiter([node1], "**", "bold")
        rnode1 = [TextNode("Greetings ", "text"), TextNode("Bold", "bold"), TextNode(" Text!", "text")]
        self.assertEqual(snode1, rnode1)

    def test_start_split_nodes_delimiter(self):
        #Test case where the *italic* text is at the start
        node1 = TextNode("*Greetings* Bold Text And *Another*", "text")
        snode1 = split_nodes_delimiter([node1], "*", "italic")
        rnode1 = [TextNode("Greetings", "italic"), TextNode(" Bold Text And ", "text"), TextNode("Another", "italic")]
        self.assertEqual(snode1, rnode1)

    def test_wrong_split_nodes_delimiter(self):
        #Test case with **bold** text but *italic* delimiter. Expect ValueError
        node1 = [TextNode("Greetings **Bold** Text!", "text")]
        snode1 = split_nodes_delimiter(node1, "*", "italic")
        self.assertEqual(node1, snode1)

    def test_single_split_nodes_delimiter(self):
        #Test case with a single asterisk and *italic* delimiter. Should not execute the regular str.split() method.
        node1 = TextNode("Greetings * regular text!", "text")
        snode1 = split_nodes_delimiter([node1], "*", "italic")
        rnode1 = [TextNode("Greetings * regular text!", "text")]
        self.assertEqual(snode1, rnode1)

    def test_no_split_nodes_delimiter(self):
        #Test case with no delimiter
        node1 = [TextNode("Greetings Bold Text!", "text")]
        snode1 = split_nodes_delimiter(node1, "*", "italic")
        self.assertEqual(node1, snode1)

    def test_twin_split_nodes_delimiter(self):
        node1 = TextNode("We **test** two **emboldened** fragments.", "text")
        snode1 = split_nodes_delimiter([node1], "**", "bold")
        rnode1 = [TextNode("We ", "text"), TextNode("test", "bold"), TextNode(" two ", "text"), TextNode("emboldened", "bold"), TextNode(" fragments.", "text")]
        self.assertEqual(snode1, rnode1)

    def test_escaped_split_nodes_delimiter(self):
        node1 = [TextNode(r"This is a sentence \*with fake italic\*. Will it work?", "text")]
        snode1 = split_nodes_delimiter(node1, "*", "italic")
        self.assertEqual(node1, snode1)

    def test_split_nodes_delimiter_image(self):
        node1 = TextNode("This sentence contains an image: ![alt](www.image.com).", "text")
        snode1 = split_nodes_delimiter([node1], "[", "image")
        rnode1 = [TextNode("This sentence contains an image: ", "text"), TextNode("alt", "image", "www.image.com"), TextNode(".", "text")]
        self.assertEqual(snode1, rnode1)

    def test_SND_link(self):
        node1 = TextNode("This sentence contains a [hyperlink to hell](www.hell.com).", "text")
        snode1 = split_nodes_delimiter([node1], "[", "link")
        rnode1 = [TextNode("This sentence contains a ", "text"), TextNode("hyperlink to hell", "link", "www.hell.com"), TextNode(".", "text")]
        self.assertEqual(snode1, rnode1)

    def test_SND_mixed(self):
        node1 = TextNode("This sentence contains an image: ![alt](www.image.com) and a [hyperlink](www.google.com).", "text")
        snode1 = split_nodes_delimiter([node1], "[", "image")
        rnode1 = [TextNode("This sentence contains an image: ", "text"), TextNode("alt", "image", "www.image.com"), TextNode(" and a [hyperlink](www.google.com).", "text")]
        self.assertEqual(snode1, rnode1)


if __name__ == "__main__":
    unittest.main()
