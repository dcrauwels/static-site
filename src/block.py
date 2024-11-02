from htmlnode import HTMLNode, LeafNode, ParentNode

def markdown_to_blocks(markdown: str) -> list:
    # converts an input string (assumed to be in markdown format) into a list of paragraph strings
    # retuns a list of strings
    # markdown denotes paragraphs by inserting a newline in between
    # the result should therefore concatenate multiple strings in a block through the use of \n as a single string in the result list
    # also excessive newlines (two or more) are ignored

    result = [] #result holder
    block_holder = ""
    for line in markdown.split("\n"): #iterate over lines
        if line == "" and len(block_holder) > 0: #check if we don't have a leading empty line. if it's not a leading line, empty line means a new block starts
            result.append(block_holder.strip())
            block_holder = ""
        else:
            block_holder += line + "\n"
    
    if len(block_holder) > 0:
        result.append(block_holder.strip())
    
    return result

def block_to_block_type(block: str) -> str:
    # takes a single block of markdown text as generated from markdown_to_blocks()
    # returns a string containing one of the following which describes the block type:
    # [paragraph, heading, code, quote, unordered_list, ordered_list]
    # basically just go over all the conditions (starting characters, sometimes ending)
    # and return a string depending on the match

    split_block = block.split("\n")
    
    # Heading
    # I'll use regex for the one to six # characters
    import re
    re_heading = re.match(r"#{1,6}", block)
    if re_heading is not None:
        return "heading"

    # Code
    if block[0:3] == "```" and block[-3:] == "```":
        return "code"

    # Quote
    # this one is hard. every line in a quote starts with >
    # so two conditions:
    # 1. first character is >
    # 2. every \n is followed by >
    # will do this by temporarily splitting the block, iterating over all lines
    for line in split_block: 
        if line[0] != ">":
            break
    else: # note: this else executes only if the break directly above it wasn't called
        return "quote"

    # Unordered List
    # same idea as quote
    for line in split_block:
        if line[0:2] != "* " and line[0:2] != "- ":
            break
    else:
        return "unordered_list"

    # Ordered List
    # a bit harder than ulist, because we also need to track the order
    order = 1
    for line in split_block:
        if line[0:3] != f"{order}. ":
            break
        order += 1
    else:
        return "ordered_list"

    # Paragraph
    # if none of the other types are returned, it's a paragraph
    return "paragraph"

def markdown_to_html_node(markdown: str) -> ParentNode:
    # Converts a markdown text in str format to an ParentNode
    from textnode import text_to_textnodes, text_node_to_html_node
    
    # convert the contained text (value) using text_to_textnode()
    def text_to_children(text: str) -> list:
        # converts a chunk of text to a list of HTMLNode children
        # used in each of the functions below
        result = []
        nodes = text_to_textnodes(text)
        for n in nodes:
            result.append(text_node_to_html_node(n))
        return result

    # Subfunctions for block types
    ## heading
    def heading_to_html_node(block: str) -> ParentNode:
        # need to check how many actual leading # the block has
        # assume headings do not contain 
        import re
        level = len(re.search(r"(#+) ", block)[1])
        return ParentNode(f"h{level}", text_to_children(block[level+1:]))

    ## code
    def code_to_html_node(block: str) -> ParentNode:
        # code blocks should be surrounded by a <code> tag nested inside a <pre> tag
        l = ParentNode("code", text_to_children(block[4:-3]))
        return ParentNode("pre", [l])

    ## quote
    def quote_to_html_node(block: str) -> ParentNode:
        #quote blocks should be surrounded by a blockquote tag
        #remember: each line in a block quote has a leading "> "
        stripped_block = []
        for line in block.split("\n"):
            stripped_block.append(line[2:])
        stripped_block = "\n".join(stripped_block)
        return ParentNode("blockquote", text_to_children(stripped_block))

    ## unordered list
    def ulist_to_html_node(block: str) -> ParentNode:
        # each of the list items needs to be made into a separate <li> htmlnode
        # with a surrounding <ul> htmlnode
        list_items = []
        for line in block.split("\n"):
            list_items.append(ParentNode("li", text_to_children(line[2:])))
        return ParentNode("ul", list_items)

    ## ordered list
    def olist_to_html_node(block: str) -> ParentNode:
        # each of the list items needs to be made into a separate <li> htmlnode
        # with a surrounding <ol> htmlnode
        list_items = []
        for line in block.split("\n"):
            list_items.append(ParentNode("li", text_to_children(line[3:])))
        return ParentNode("ol", list_items)

    ## paragraph
    def paragraph_to_html_node(block: str) -> ParentNode:
        return ParentNode("p", text_to_children(' '.join(block.split())))

    # Call appropriate function for respective block type
    ## first we make a list with structure [[block, block_type],...]
    blocks = [[b, block_to_block_type(b)] for b in markdown_to_blocks(markdown)]   
    content = []
    ## Then call the correct function
    for b in blocks:
        if b[1] == "heading":
            content.append(heading_to_html_node(b[0]))
        if b[1] == "code":
            content.append(code_to_html_node(b[0]))
        if b[1] == "quote":
            content.append(quote_to_html_node(b[0]))
        if b[1] == "unordered_list":
            content.append(ulist_to_html_node(b[0]))
        if b[1] == "ordered_list":
            content.append(olist_to_html_node(b[0]))
        if b[1] == "paragraph":
            content.append(paragraph_to_html_node(b[0]))

    # Finally export as a containing div
    return ParentNode("div", content)
