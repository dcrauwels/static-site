def markdown_to_blocks(markdown: str) -> list:
    # converts an input string (assumed to be in markdown format) into a list of paragraph strings
    # markdown denotes paragraphs by inserting a newline in between
    # the result should therefore concatenate multiple strings in a block through the use of \n as a single string in the result list
    # also excessive newlines (two or more) are ignored

    result = [] #result holder
    block_counter = 0 #oh god
    for line in markdown.split("\n"): #iterate over lines
        if line == "" and len(result) > 0: #check if we don't have a leading empty line. if so, empty line = new block = block_counter++
            
            result[block_counter] = result[block_counter][:-2] #remove trailing newline
            block_counter += 1
        result[block_counter] += line + "\n"
    result[block_counter] = result[block_counter][:-2] #for good measure
    return result
