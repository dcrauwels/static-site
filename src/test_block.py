import unittest
from block import markdown_to_blocks, block_to_block_type, markdown_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode

class TestTextNode(unittest.TestCase):
    def test_block_simple(self):
        text1 = "This is a sample sentence.\nThis is still the same block.\n\nThis is a new block."
        block1 = markdown_to_blocks(text1)
        rblock1 = ["This is a sample sentence. This is still the same block.", "This is a new block."]
        self.assertEqual(block1, rblock1)
    
    def test_block_empty(self):
        text1 = "\n\n\n\n\n\n"
        block1 = markdown_to_blocks(text1)
        rblock1 = []
        self.assertEqual(block1,rblock1)

    def test_BTBT_simple(self):
        block1 = "Regular paragraph."
        type1 = block_to_block_type(block1)
        rtype1 = "paragraph"
        self.assertEqual(type1, rtype1)

    def test_BTBT_olist_correct(self):
        block1 = "1. First item\n2. Second item\n3. Third item"
        type1 = block_to_block_type(block1)
        rtype1 = "ordered_list"
        self.assertEqual(type1, rtype1)

    def test_BTBT_olist_correct(self):
        block1 = "1. First item\n2.Second item\n3. Third item"
        type1 = block_to_block_type(block1)
        rtype1 = "paragraph"
        self.assertEqual(type1, rtype1)

    def test_MTB_BTBT_pipeline(self):
        text1 = "```Single block code paragraph\nWith a lot of text\nEnding in three backticks```"
        block1 = markdown_to_blocks(text1)
        type1 = block_to_block_type(block1[0])
        rtype1 = "code"
        self.assertEqual(type1, rtype1)

    def test_markdown_to_html_node_basic(self):
        text1 = "# Heading\n\n- Hi\n- I'm\n- Daisy\n\nRegular *paragraph*"
        node1 = markdown_to_html_node(text1)
        rnode1 = ParentNode(
                "div",
                [
                    ParentNode(
                        "h1", [LeafNode(None, "Heading")]
                        ),
                    ParentNode(
                        "ul", [
                            ParentNode("li", [LeafNode(None, "Hi")]),
                            ParentNode("li", [LeafNode(None, "I'm")]),
                            ParentNode("li", [LeafNode(None, "Daisy")])
                            ]
                        ),
                    ParentNode(
                        "p", [
                            LeafNode(None, "Regular "),
                            LeafNode("i", "paragraph")
                            ]
                        )
                    ]
                )
        self.assertEqual(node1, rnode1)




if __name__ == "__main__":
    unittest.main()
