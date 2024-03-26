from textnode import TextNode
from htmlnode import HTMLNode

def main():
    test_textnode = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(test_textnode)
    test_htmlnode = HTMLNode("a", "Some link text", None, {"href": "www.google.com"})
    print(test_htmlnode)
    print(test_htmlnode.props_to_html())


if __name__ == "__main__":
    main()
