def markdown_to_blocks(markdown: str) -> list:
    # converts an input string (assumed to be in markdown format) into a list of paragraph strings
    # markdown denotes paragraphs by inserting a newline in between
    # the result should therefore concatenate multiple strings in a block through the use of \n as a single string in the result list
    # also excessive newlines (two or more) are ignored

    result = [] #result holder
    block_holder = ""
    for line in markdown.split("\n"): #iterate over lines
        if line == "" and len(block_holder) > 0: #check if we don't have a leading empty line. if so, empty line = new block = block_counter++
            result.append(block_holder.strip())
            block_holder = ""
        elif line != "":
            block_holder += line + " "
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
