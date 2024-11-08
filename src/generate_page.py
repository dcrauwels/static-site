

def extract_title(markdown: str) -> str:
    # extracts a heading level 1 string from a markdown formatted text.
    # this is formatted in md as:
    #   # heading
    # returns a string without the leading # or whitespace


    for line in markdown.split('\n'):
        if line[0:2] == '# ':
            return line[1:].lstrip(' ')
        else:
            raise Exception('No header found.')


def generate_page(
        from_path: str = "content/index.md", 
        template_path: str = "template.html", 
        dest_path: str = "public/index.html"
        ) -> None:
    # Generates an html page based on a markdown file in from_path and a template html document in html_path.

    # Imports
    from block import markdown_to_html_node
    from os import makedirs, path

    # Escapes
    ## Check for completely empty paths.
    if 0 in [len(x) for x in [from_path, template_path, dest_path]]:
        raise ValueError('Incorrect path specified.')

    ## Append filenames to paths if none are given.
    if from_path[-1] == "/":
        from_path += "index.md"
    if template_path[-1] == "/":
        template_path += "template.html"
    if dest_path[-1] == "/":
        dest_path += "index.html"

    # Print message to stdout so we know what's happening
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read files
    with open(from_path, 'r') as md_file, open(template_path, 'r') as template_file:
        markdown = md_file.read()
        template = template_file.read()

    # Process markdown into HTMLnodes using markdown_to_html_node
    mk_to_htmlnode = markdown_to_html_node(markdown)

    # Then HTMLnode into HTML using .to_html() method
    content = mk_to_htmlnode.to_html()

    # Get title from markdown
    title = extract_title(markdown)

    # Populate template
    output = "" # initialize empty string
    ## Replace {{ Title }} with title (extract_title())
    output = template.replace('{{ Title }}', title)

    ## Replace {{ Content }} with content (markdown_to_html_node().to_html())
    output = output.replace('{{ Content }}', content)

    # Write full HTML page to dest_path
    ## Check if required directories exist, mkdir if needed
    makedirs(path.dirname(dest_path), exist_ok = True)

    #dest_split = dest_path.split('/')
    #for i in range(len(dest_split)):
    #    current_path = dest_split[i]
    #    if not path.exists(current_path):
    #        makedirs(current_path)

    #    if not i == len(dest_split):
    #        current_path = path.join(current_path, dest_split[i+1]


    ## Write actual HTML page
    with open(dest_path, 'w') as f:
        f.write(output)

    # return
    print("Page generated.")
    return

def generate_pages_recursive(
        dir_path_content: str = "content",
        template_path: str = "template.html",
        dest_dir_path:str = "public"
        ):
    # Generates pages recursively by crawling entire directory.
    # calls generate_page per .md file found.
    
    # imports
    import os
    import shutil

    # clean up existing destination directory
    if os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)
    os.mkdir(dest_dir_path)

    # generate recursively
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dst_path = os.path.join(dest_dir_path, item)
        html_extended = item[:item.rfind('.')] + ".html"
        html_path = os.path.join(dest_dir_path, html_extended)

        if src_path[-3:] == ".md":
            generate_page(src_path, template_path, html_path)
        elif not os.path.isfile(src_path):
            generate_pages_recursive(src_path, template_path, dst_path)

    return
