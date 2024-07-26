from htmlnode import LeafNode
from textnode import TextNode
from textnode import (text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image)


def text_node_to_html_node(text_node):
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

# Does not support nested delimiters
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    valid = [text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image]
    if text_type not in valid:
        raise Exception(f"unsupported text type: {text_type}")
   
    parts = old_nodes.split(delimiter)
    nodes = []

    for i, part in enumerate(parts):
        if i % 2 == 0:
            # Non-delimited part
            nodes.append(TextNode(part, text_type_text))
        else:
            # Delimited part
            nodes.append(TextNode(part, text_type))

    return nodes