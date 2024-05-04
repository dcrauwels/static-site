import unittest
from block import markdown_to_blocks

class TestTextNode(unittest.TestCase):
    def test_block_simple(self):
        text1 = "This is a sample sentence.\nThis is still the same block.\n\nThis is a new block."
        block1 = markdown_to_blocks(text1)
        rblock1 = ["This is a sample sentence. This is still the same block. ", "This is a new block. "]
        self.assertEqual(block1, rblock1)

if __name__ == "__main__":
    unittest.main()
