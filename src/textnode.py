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
            delimiter_found = False
            if not (i == len(o.text) and len(delimiter) > 1): # str out of bounds
                delimiter_found = (
                        delimiter == o.text[i:i+len(delimiter)] and # delimiter matches text from i, moving forward
                        delimiter != o.text[i+1:i+len(delimiter)+1] and # delimiter does not appear after i
                        delimiter != o.text[i-len(delimiter):i] # delimiter does not appear before i
                        )
            escape_found = False
            if i > 0: # str out of bounds (negative wrap really)
                escape_found = o.text[i-1] == "\\"
            if delimiter_found and not escape_found: 
                any_delimiters = True
                delimiters_counted.append(i)
                # Images and links use a [text](url) format in MD, so the delimiter needs to be dynamically updated.
                # This shifts the delimiter to the next in a sequence of []() characters with a modulus to overflow and reset when we reach ).
                if delimiter in hyperlink_delimiters:
                    delimiter = hyperlink_delimiters[(hyperlink_delimiters.index(delimiter) + 1) % len(hyperlink_delimiters)]

        # Payoff starts here. First we init, then enter the while loop
        o_tail = o
        new_nodes = []

        # When two or more delimiters found
        while len(delimiters_counted) >= 2:
            # First append the part leading up to the first delimiter found.     
            new_nodes.append(o_tail[0:delimiters_counted[0]]) #see __getitem__ implementation in TextNode class for subscripting.
            
            # Then append the node content
            new_nodes.append(TextNode(o_tail.text[delimiters_counted[0]+len(delimiter) : delimiters_counted[1]], text_type)) 

            # Filter out empty nodes. Needed in case the string starts with a delimiter.
            new_nodes = [n for n in new_nodes if n.text != ""] 

            # Update the o_tail container. Either for appending tail or second delimited section.
            o_tail = o_tail[delimiters_counted[1]+len(delimiter):] 
            # And update the indices of the delimiters_counted list as the o_tail referenced by these indices has shifted accordingly.
            delimiters_counted = [x - delimiters_counted[1]-len(delimiter) for x in delimiters_counted] 

            # Delete the two delimiter indices used for this run of the while loop.
            del delimiters_counted[0:2] # Reset the delimiters_counted list in case we find another delimited section
        
        result.extend(new_nodes) # Payoff for delimited substrings
        
        # Payoff for remaining tail of o_tail
        if o_tail.text != "":
            result.append(o_tail)
            
        # Tidyness check for when delimiter is not found. Still doesn't do the trick for delimiter = * and **bold** text appears.
        if not any_delimiters: 
            raise ValueError(f"Delimiter {delimiter} not found in node {o}.")
        else:
            return result

def split_nodes_image(old_nodes:list) -> list:
    # Returns a list of TextNodes with images properly implemented. We'll do this by calling split_nodes_delimiter() and fixing the output.
    # This entails two steps:
    # 1. Remove the leading exclamation mark (!) for images in MD from the TextNode(..., "text") preceding the image tag.
    # 1.1. Note that this means we need to check if the TextNode(..., "text") in question is empty after doing so. (This means the original TextNode started with an image.)
    # 2. Concatenate the two instances of TextNode(..., "image") split_nodes_delimiter will find.
    
    # Init result list
    
    new_nodes = []
    for o in old_nodes:
        if len(extract.extract_markdown_links(o.text)) == 0:
            new_nodes.append(o)
    
    if len(new_nodes) == 0:
        return []

    split_nodes = split_nodes_delimiter(new_nodes, "[", "image")
    
    # Loop over nodes to find image TextNode positions
    image_positions = []
    for i in range(len(split_nodes)):
        if split_nodes[i].text_type == "image":
            image_positions.append(i)

    while len(image_positions) >= 2:
        # 2. Concatenate the two instances of TextNode
        concat_node = TextNode(split_nodes[image_positions[0]].text, "image", split_nodes[image_positions[1]].text)
        split_nodes[image_positions[0]] = concat_node
        
        del split_nodes[image_positions[1]]

        # 1. Remove the leading exclamation mark
        split_nodes[image_positions[0]-1].text = split_nodes[image_positions[0]-1].text[:-1]
        # 1.1 Check if resulting TextNode is empty
        if split_nodes[image_positions[0]-1].text == "":
            del split_nodes[image_positions[0]-1]

        # Update image_positions list
        image_positions = list(map(lambda x: x-1, image_positions))
        del image_positions[0:2]

    return split_nodes

def split_nodes_link(old_nodes: list) -> list:
    # Returns a list of TextNodes with links properly implemented. Copy of split_nodes_image(). Refer to that function for comments.
    
    new_nodes = []
    for o in old_nodes:
        if len(extract.extract_markdown_images(o.text)) == 0:
            new_nodes.append(o)

    if len(new_nodes) == 0:
        return []

    split_nodes = split_nodes_delimiter(new_nodes, "[", "link")
    link_positions = []

    for i in range(len(split_nodes)):
        if split_nodes[i].text_type == "link":
            link_positions.append(i)

    while len(link_positions) >= 2:
        concat_node = TextNode(split_nodes[link_positions[0]].text, "link", split_nodes[link_positions[1]].text)
        split_nodes[link_positions[0]] = concat_node
        del split_nodes[link_positions[1]]
        link_positions = list(map(lambda x: x-1, link_positions))
        del link_positions[0:2]

    return split_nodes
