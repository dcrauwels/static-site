import unittest
from generate_page import extract_title, generate_page

class TestTextNode(unittest.TestCase):
    def extract_title_simple(self):
        text1 = "Hi I'm daisy.\n# This is a heading.\n#This is not a heading.\n## This is, but it's not a title."
        title1 = extract_title(text1)
        rtitle1 = "This is a heading."
        self.assertEqual(title1, rtitle1)

    def extract_title_leadingspace(self):
        text1 = "#     This is a title with many leading spaces."
        title1 = extract_title(text1)
        rtitle1 = "This is a title with many leading spaces."
        self.assertEqual(title1, rtitle1)

