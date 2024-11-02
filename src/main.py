from textnode import TextNode
from htmlnode import HTMLNode
import copy_static
from generate_page import generate_page

def main():
    copy_static.main()
    generate_page()

if __name__ == "__main__":
    main()
