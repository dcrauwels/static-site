from htmlnode import LeafNode

class TextNode:
    # Models a Markdown string.
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        if isinstance(node, TextNode):
            return self.text == node.text and self.text_type == node.text_type and self.url == node.url
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    # Converts a TextNode to a LeafNode based on the TextNode.text_type attribute.
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text)
    if text_node.text_type == "bold":
        return LeafNode("b", text_node.text)
    if text_node.text_type == "italic":
        return LeafNode("i", text_node.text)
    if text_node.text_type == "code":
        return LeafNode("code", text_node.text)
    if text_node.text_type == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt":text_node.text})
    raise TypeError(f"Text Node has invalid type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # Splits a TextNode into a list of TextNodes with appropriate text_types based on a delimiter. Currently needs the delimiter and text_type to be provided manually.
    result = []
    for o in old_nodes:
        if type(o) != "TextNode":
            result.append(o)
        if delimiter not in o:
            raise ValueError(f"Delimiter {delimiter} not found in node {o}.")
        for chunk in enumerate(o.text.split(delimiter)): # Use enumerate to track even/odd
            if chunk[0] % 2 == 0:
                result.append(TextNode(chunk[1], "text"))
            else:
                result.append(TextNode(chunk[1], text_type))
    return result
