from htmlnode import LeafNode

def text_node_to_html_node(text_node):

    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_link = "link"
    text_type_image = "image"

    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text, None)
    
    elif text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text, None)

    elif text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text, None)
    
    elif text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text, None)
    
    elif text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    
    elif text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("unsupported or no text type in text node")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    pass 