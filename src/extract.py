import re
# Don't think I need these two libraries yet.
#import textnode
#import htmlnode

def extract_markdown_images(text: str) -> list:
    # Returns a list of tuples containing (alt text, image url). In markdown, an image is formatted as ![ALT](IMAGE_URL).
    # Will use regex to extract the alt text and url. Regex string should detect:
    # 1. !
    # 2. [
    # 3. Capture group 1: alt text
    # 4. ]
    # 5. (
    # 6. Capture group 2: image url
    # 7. )
    # In summary: !\[(.*?)\]\((.*?)\)
    
    reg_str = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(reg_str, text)

def extract_markdown_links(text: str) -> list:
    # Returns a list of tuples containing (anchor text, url). In markdown, a hyperlink is formatted as [ANCHOR_TEXT](URL).
    # Will use regex to extract the alt text and url. Based on previous, regex string should be:
    # \[(.*?)\][((.*?)\)

    reg_str = r"[^!]\[(.*?)\]\((.*?)\)"
    return re.findall(reg_str, text)
