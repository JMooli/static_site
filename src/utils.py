import os
import pathlib
import re
from htmlnode import *
from textnode import TextNode
from textnode import (text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image)

heading_pattern = re.compile(r'^(#+) ')

def count_initial_hashes(s):
    match = heading_pattern.match(s)
    if match:
        return len(match.group(1))
    else:
        return 0

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

    valid = [text_type_text, text_type_bold, text_type_italic, text_type_code]
    if text_type not in valid:
        raise Exception(f"unsupported text type: {text_type}")
    
    nodes = []

    for node in old_nodes:
        if node.text_type == text_type_text:
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    # Non-delimited part
                    nodes.append(TextNode(part, text_type_text))
                else:
                    # Delimited part
                    nodes.append(TextNode(part, text_type))
        else:
            nodes.append(node)
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

def text_to_textnodes(text):
    # Split text into nodes
    nodes = []
    nodes.append(TextNode(text, text_type_text))
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    # paragraph
    # heading
    # code
    # quote
    # unordered_list
    # ordered_list

    if count_initial_hashes(block) > 0 and count_initial_hashes(block) < 6:
        return "heading"
    elif block[:3] == "```" and block[-3:] == "```":
        return "code"
    elif block[0] == ">":
        is_quote = True
        for line in block.split("\n"):
            if line[0] != ">":
                is_quote = False
        if is_quote:
            return "quote"

    elif block.startswith("* ") or block.startswith("- "):
        return "unordered_list"
    
    elif block.split(". ")[0].isdigit():
        order = int(block.split(". ")[0])
        is_ordeded = True
        for line in block.split("\n"):
            parts = line.split(". ")
            if parts[0].isdigit():
                if int(parts[0]) -1 == order:
                    order = int(parts[0]) 
            else:
                is_ordeded = False
        if is_ordeded:
            return "ordered_list"
    else: 
        return "paragraph"

def markdown_to_html_node(markdown):

    def block_to_html_paragraph(block):
        return ParentNode("p", children=text_to_children(block))

    # need to add h1, h2, etc
    def block_to_html_heading(block):
        hashes = count_initial_hashes(block)
        return LeafNode(f"h{hashes}", block.lstrip("# "))

    def block_to_html_code(block):
        return LeafNode("code", block.strip("`"))

    def block_to_html_quote(block):
        return ParentNode("blockquote", children=text_to_children(block.lstrip("> ")))

    def block_to_html_unordered_list(block):
        list_items = block.split("\n")
        child_nodes = [ParentNode("li", children=text_to_children(item.lstrip("-* "))) for item in list_items]
        return ParentNode("ul", children=child_nodes)

    def block_to_html_ordered_list(block):
        list_items = block.split("\n")
        child_nodes = [ParentNode("li", children=text_to_children(item.lstrip("0123456789. "))) for item in list_items]
        return ParentNode("ol", children=child_nodes)


    def text_to_children(text):
        text_nodes = text_to_textnodes(text)
        child_nodes = []
        for node in text_nodes:
            child_nodes.append(text_node_to_html_node(node))
        return child_nodes

    
    div_childs = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        match block_to_block_type(block):
            case "paragraph":
                div_childs.append(block_to_html_paragraph(block))
            case "heading":
                div_childs.append(block_to_html_heading(block))
            case "code":
                div_childs.append(block_to_html_code(block))
            case "quote":
                div_childs.append(block_to_html_quote(block))
            case "unordered_list":
                div_childs.append(block_to_html_unordered_list(block))
            case "ordered_list":
                div_childs.append(block_to_html_ordered_list(block))
    
    return ParentNode("div", children=div_childs)

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line.lstrip("# ")
    raise Exception("No header found !")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as f_md:
        markdown = f_md.read()
    
    with open(template_path, 'r') as f_t:
        template = f_t.read()

    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html_content = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f_out:
        f_out.write(html_content)

def generate_pages_recursive(content_dir, template_path, dest_dir_path):
    dir_path_content = os.listdir(content_dir)
    for file in dir_path_content:
        file_path = pathlib.Path(content_dir, file)
        dest_path = pathlib.Path(dest_dir_path, file)
        if os.path.isfile(file_path):
            if file.split(".")[-1] == "md":
                dest_path = pathlib.Path(dest_dir_path, file.replace(".md", ".html"))
                generate_page(file_path, template_path, dest_path)
        else:
            generate_pages_recursive(file_path, template_path, dest_path)

        