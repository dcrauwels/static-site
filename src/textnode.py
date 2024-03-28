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
        return f"TextNode(\"{self.text}\", {self.text_type}, {self.url})"

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

    raise TypeError(f"Text Node has invalid type: {text_node.text_type}") # Catch-all if no return is taken earlier

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # Splits a TextNode into a list of TextNodes with appropriate text_types based on a delimiter. Currently needs the delimiter and text_type to be provided manually.
    result = []

    for o in old_nodes:
        # Escapes
        if not isinstance(o, TextNode): #Kind of an escape if we get unexpected items in the old_nodes list
            result.append(o)
        if delimiter not in o.text: #Escape for when delimiter is not found. Still doesn't do the trick for delimiter = * and **bold** text appears.
            raise ValueError(f"Delimiter {delimiter} not found in node {o}.")

        ## I could implement this entire loop as a subfunction to also lift out the image/link url, which is not supported right now.

        # Scroll over the entirity of o.text while tracking delimiters in delimiter_counted
        delimiters_counted = []
        for i in range(len(o.text)):
            
            # Check if delimiter is found and is not escaped -> append to delimiters_counted list
            print(o.text[i:i+len(delimiter)])

            delimiter_found = False
            if not (i == len(o.text) and len(delimiter) > 1): # str out of bounds
                delimiter_found = delimiter == o.text[i:i+len(delimiter)] and delimiter != o.text[i+1:i+len(delimiter)+1]
            escape_found = False
            if i > 0: # str out of bounds (negative wrap really)
                escape_found = o.text[i-1] != "\\"
            if delimiter_found and not escape_found: 
                print(f"Delimiter found at index {i}: {o.text[i:i+len(delimiter)]}")
                delimiters_counted.append(i)
                if text_type == "link" or text_type == "image": # For links and images
                    delimiter = "]"
            
            # When two delimiters found: we split only the relevant part
            if len(delimiters_counted) == 2:
                new_nodes = o.text[delimiters_counted[0]:delimiters_counted[1]+1].split(delimiter)
                for node in enumerate([n for n in new_nodes if n!= ""]): # Use enumerate to track even/odd and list comprehension to filter out empty items
                    if (node[0] % 2) == 0: 
                        result.append(TextNode(node[1], "text"))
                    else:
                        result.append(TextNode(node[1], text_type))
                o = o[delimiters_counted[1]:] # We'll need this to append the tail of o.text

                delimiters_counted = [] # Reset the delimiters_counted list in case we find another marked section
                if text_type == "link" or text_type == "image": # For links and images
                    delimiter = "["

        # Append remaining tail of o to result
        result.append(o)
        
    return result
