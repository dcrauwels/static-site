from textnode import TextNode
from htmlnode import HTMLNode
import copy_static
from generate_page import generate_pages_recursive

def main():
    copy_static.main()
    generate_pages_recursive()

if __name__ == "__main__":
    main()
