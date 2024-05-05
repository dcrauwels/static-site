class HTMLNode:
    # Represents an HTML node with a leading and closing tag.
    # Tag is <a>, <p>, etc.
    # Value is the content in between the tags
    # Children are HTMLNodes contained in the larger node. I.e. the parent node is <div>
    # props are the attributes for a tag. Like href="www.google.com"
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Method not implemented on HTMLNode")

    def props_to_html(self):
        result = ""
        if self.props is not None:
            for key, value in self.props.items():
                result += f" {key}=\"{value}\""
        return result

    def __eq__(self, node):
        if isinstance(node, HTMLNode):
            return self.tag == node.tag and self.value == node.value and self.children == node.children and self.props == node.props
        return False

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    # LeafNodes are leaf nodes, i.e. nodes without children
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: value missing")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    # ParentNodes contain LeafNodes
    # does not have a value
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag not provided. ParentNodes should have children - i.e. should be nesting LeafNodes inside tags.")
        if self.children is None:
            raise ValueError("Children not provided. ParentNodes should have children.")
        result = f"<{self.tag}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"
        return result

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"


