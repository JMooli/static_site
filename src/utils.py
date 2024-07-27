import re

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

def extract_markdown_images(text):
    # ![alt text for image](url/of/image.jpg)
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    # This is a paragraph with a [link](https://www.google.com).
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def recursive_split(string, images, index=0):

    if index >= len(images):
        return [string]

    parts = string.split(images[index])
    split_parts = [recursive_split(part, images, index + 1) for part in parts]
    flattened_parts = [item for sublist in split_parts for item in sublist]

    return flattened_parts


def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        images = extract_markdown_images(node.text)

        if images:
            image_delimiters = [f"![{image[0]}]({image[1]})" for image in images]
            parts = recursive_split(node.text, image_delimiters)

            for i in range(len(parts)):
                if parts[i] != "":
                    new_nodes.append(TextNode(parts[i], text_type_text))
                if i < len(images):
                    new_nodes.append(TextNode(images[i][0], text_type_image, images[i][1]))
        else:
            new_nodes.append(node)
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        links = extract_markdown_links(node.text)

        if links:
            link_delimiters = [f"[{link[0]}]({link[1]})" for link in links]
            parts = recursive_split(node.text, link_delimiters)

            for i in range(len(parts)):
                if parts[i] != "":
                    new_nodes.append(TextNode(parts[i], text_type_text))
                if i < len(links):
                    new_nodes.append(TextNode(links[i][0], text_type_link, links[i][1]))
        else:
            new_nodes.append(node)
    
    return new_nodes