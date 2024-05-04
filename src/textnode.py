from htmlnode import LeafNode
import extract

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

    def __getitem__(self, item):
        return TextNode(self.text[item], self.text_type, self.url)

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
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

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: str) -> list:
    # Splits a TextNode into a list of TextNodes with appropriate text_types based on a delimiter. Currently needs the delimiter and text_type to be provided manually.
    result = []
    image_or_link = text_type in ["image", "link"]
    hyperlink_delimiters = ["[", "]", "(", ")"]

    for o in old_nodes:
        # Escapes
        if not isinstance(o, TextNode): #Kind of an escape if we get unexpected items in the old_nodes list
            result.append(o)
        any_delimiters = False
        ## I could implement this entire loop as a subfunction to also lift out the image/link url, which is not supported right now.

        # Scroll over the entirity of o.text while tracking delimiters in delimiter_counted
        delimiters_counted = []
        for i in range(len(o.text)):
            
            # Check if delimiter is found and is not escaped -> append to delimiters_counted list
            # First check for the escape
            if i > 0: # prevent negative wrap mishaps 
                if o.text[i-1] == "\\":
                    continue #just pass on to the next character if this one is escaped
            
            # Then check for the delimiter itself
            delimiter_found = False
            if not (i == len(o.text) and len(delimiter) > 1): # str out of bounds
                delimiter_found = (
                        delimiter == o.text[i:i+len(delimiter)] and # delimiter matches text from i, moving forward if len > 1
                        delimiter != o.text[i+1:i+len(delimiter)+1] and # delimiter does not appear directly after i
                        delimiter != o.text[i-len(delimiter):i] # delimiter does not appear directly before i
                        ) # This is to prevent cases where **text** with delimiter * (single asterisk) is falsely interpreted as the delimiter we're looking for.
            if delimiter_found:
                any_delimiters = True # This is for a tidyness check all the way at the end. We return an error if this function is used on a sentence without the delimiter we're looking for.
                delimiters_counted.append(i)
                # This shifts the delimiter to the next in a sequence of []() characters with a modulus to overflow and reset when we reach ).
                if text_type in ["image", "link"]:
                    delimiter = hyperlink_delimiters[(hyperlink_delimiters.index(delimiter) + 1) % len(hyperlink_delimiters)]

        # Payoff starts here. First we init, then enter the while loop
        o_tail = o
        new_nodes = []

        # When two or more delimiters found for non-image or -link type splits
        while len(delimiters_counted) >= 2: 
            # First append the part leading up to the first delimiter found.     
            new_nodes.append(o_tail[0:(delimiters_counted[0] - int(text_type == "image"))]) # The boolean to int conversion is to ditch the exclamation mark preceding an image tag.
            
            # Then append the node content. Two cases: regular and image/link
            # image/link
            if image_or_link and len(delimiters_counted) >= 4:
                if text_type == "image":
                    nn = extract.extract_markdown_images(o_tail.text) 
                elif text_type == "link":
                    nn = extract.extract_markdown_links(o_tail.text)
                new_nodes.append(TextNode(nn[0][0], text_type, nn[0][1])) # Note that these may identify multiple images. So nn[0][i] where i=0 for alt and i=1 for url.
            # regular
            else:
                new_nodes.append(TextNode(o_tail.text[delimiters_counted[0]+len(delimiter) : delimiters_counted[1]], text_type)) 

            # Filter out empty nodes. Needed in case the string starts with a delimiter.
            new_nodes = [n for n in new_nodes if n.text != ""] 

            # Update the o_tail container. Either for appending tail or second delimited section.
            next_node_index = 3 if image_or_link else 1 # This is because we count 4 delimiters for images and links, and 2 for the other text_types
            o_tail = o_tail[delimiters_counted[next_node_index]+len(delimiter):] 
            # And update the indices of the delimiters_counted list as the o_tail referenced by these indices has shifted accordingly.
            delimiters_counted = [x - delimiters_counted[next_node_index]-len(delimiter) for x in delimiters_counted] 

            # Delete the two or four delimiter indices used for this run of the while loop.
            del delimiters_counted[0:(next_node_index+1)] # Reset the delimiters_counted list in case we find another delimited section

        result.extend(new_nodes) # Payoff for delimited substrings
        
        # Payoff for remaining tail of o_tail
        if o_tail.text != "":
            result.append(o_tail)
            
        # Tidyness check for when delimiter is not found. Still doesn't do the trick for delimiter = * and **bold** text appears.
        if not any_delimiters: 
            raise ValueError(f"Delimiter {delimiter} not found in node {o}.")
        else:
            return result

