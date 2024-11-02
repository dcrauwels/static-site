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
            continue
        if o.text == "":
            result.append(o)
            continue
        
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
                delimiters_counted.append(i)
                # This shifts the delimiter to the next in a sequence of []() characters with a modulus to overflow and reset when we reach ).
                if image_or_link: 
                    delimiter = hyperlink_delimiters[(hyperlink_delimiters.index(delimiter) + 1) % len(hyperlink_delimiters)]

        # Payoff starts here. First we init, then enter the while loop
        o_tail = o
        new_nodes = []

        # When two or more delimiters found for non-image or -link type splits
        while (not image_or_link and len(delimiters_counted) >= 2) or (image_or_link and len(delimiters_counted) >= 4): 
            # Two cases: regular and image_or_link

            # image/link
            if image_or_link and len(delimiters_counted) >= 4:
                # get a re.Match object depending on whether we are looking for images or links.
                if text_type == "image":
                    nn = extract.extract_markdown_images(o_tail.text) 
                elif text_type == "link":
                    nn = extract.extract_markdown_links(o_tail.text)
                # then process the Match object:
                # 1. append the nonmatching head of the string as o_tail[0:nn.start()]
                # 2. append the matching part of the string as a TextNode(nn.groups()[0], text_type, nn.groups()[1])
                if nn is None: # this means we have an image/link but are looking for the opposite. ergo we break immediately and append the whole thing at the end 
                    break
                if nn is not None: # re.search() returns a None object if no matches are found.
                    #new_nodes.append(o_tail[0:(nn.start() + int(text_type == "link"))]) # the bool (to int) is because the absent exclamation mark is counted for the Match.start() position
                    new_nodes.append(o_tail[0:nn.start()])
                    new_nodes.append(TextNode(nn.groups()[0], text_type, nn.groups()[1])) 
            
            # regular (bold, italic, code, etc.)
            else:
                # Same process as above:
                # 1. append nonmatching head of the string 
                # 2. append matching part of the string
                new_nodes.append(o_tail[0:delimiters_counted[0]])
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
            
    return result

def text_to_textnodes(text: str) -> list:
    # Takes a string as input and turns it into a list of TextNodes using split_nodes_delimiter().
    # Checks for each of the delimiters in turn and calls split_nodes_delimiter() for each of them. Does not seem like the way but it will work for now.
    
    # we init the result list, which will take the old_nodes parameter role in split_nodes_delimiter()
    result = [TextNode(text, "text")]
    
    # let's just run the SND() for each of the delimiters.
    result = split_nodes_delimiter(result, "*", "italic")
    result = split_nodes_delimiter(result, "**", "bold")
    result = split_nodes_delimiter(result, "`", "code")
    result = split_nodes_delimiter(result, "[", "image")
    result = split_nodes_delimiter(result, "[", "link")

    return result
