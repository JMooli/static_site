import unittest
from utils import *
from textnode import TextNode
from htmlnode import LeafNode
import sys

class TestTextNodeToHtmlNode(unittest.TestCase):

    def test_text_type_text(self):
        text_node = TextNode("This is a text node", "text", "")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_text_type_bold(self):
        text_node = TextNode("This is a bold text node", "bold", "")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        self.assertEqual(html_node.props, None)

    def test_text_type_italic(self):
        text_node = TextNode("This is an italic text node", "italic", "")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
        self.assertEqual(html_node.props, None)

    def test_text_type_code(self):
        text_node = TextNode("This is a code text node", "code", "")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
        self.assertEqual(html_node.props, None)

    def test_text_type_link(self):
        text_node = TextNode("This is a link text node", "link", "https://www.example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})

    def test_text_type_image(self):
        text_node = TextNode("This is an image text node", "image", "https://www.example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.example.com/image.png", "alt": "This is an image text node"})

    def test_unsupported_text_type(self):
        text_node = TextNode("This is an unsupported text node", "unsupported", "")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)
        self.assertTrue("unsupported or no text type in text node" in str(context.exception))

    def test_extract_markdown_images_single(self):
        text = "Here is an image: ![alt text](http://example.com/image.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "http://example.com/image.jpg")])

    def test_extract_markdown_images_multiple(self):
        text = ("Here is an image: ![image1](http://example.com/image1.jpg) "
                "and another image: ![image2](http://example.com/image2.jpg)")
        result = extract_markdown_images(text)
        self.assertEqual(result, [
            ("image1", "http://example.com/image1.jpg"),
            ("image2", "http://example.com/image2.jpg")
        ])

    def test_extract_markdown_images_no_images(self):
        text = "Here is some text without images."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_markdown_links_single(self):
        text = "Here is a link to [Google](https://www.google.com)."
        result = extract_markdown_links(text)
        self.assertEqual(result, [("Google", "https://www.google.com")])

    def test_extract_markdown_links_multiple(self):
        text = ("Here is a link to [Google](https://www.google.com) "
                "and another link to [Bing](https://www.bing.com).")
        result = extract_markdown_links(text)
        self.assertEqual(result, [
            ("Google", "https://www.google.com"),
            ("Bing", "https://www.bing.com")
        ])

    def test_extract_markdown_links_no_links(self):
        text = "Here is some text without links."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_markdown_links_and_images(self):
        text = ("Here is an image: ![alt text](http://example.com/image.jpg) "
                "and a link to [Google](https://www.google.com).")
        image_result = extract_markdown_images(text)
        link_result = extract_markdown_links(text)
        self.assertEqual(image_result, [("alt text", "http://example.com/image.jpg")])
        self.assertEqual(link_result, [("Google", "https://www.google.com")])

class TestSplitNodes(unittest.TestCase):

    def test_split_nodes_image_single(self):
        old_nodes = [TextNode("Here is an image: ![alt text](http://example.com/image.jpg)", text_type_text)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Here is an image: ")
        self.assertEqual(new_nodes[0].text_type, text_type_text)
        self.assertEqual(new_nodes[1].text, "alt text")
        self.assertEqual(new_nodes[1].text_type, text_type_image)
        self.assertEqual(new_nodes[1].url, "http://example.com/image.jpg")

    def test_split_nodes_image_multiple(self):
        old_nodes = [TextNode("Image1: ![alt1](http://example.com/image1.jpg) and Image2: ![alt2](http://example.com/image2.jpg)", text_type_text)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "Image1: ")
        self.assertEqual(new_nodes[0].text_type, text_type_text)
        self.assertEqual(new_nodes[1].text, "alt1")
        self.assertEqual(new_nodes[1].text_type, text_type_image)
        self.assertEqual(new_nodes[1].url, "http://example.com/image1.jpg")
        self.assertEqual(new_nodes[2].text, " and Image2: ")
        self.assertEqual(new_nodes[2].text_type, text_type_text)
        self.assertEqual(new_nodes[3].text, "alt2")
        self.assertEqual(new_nodes[3].text_type, text_type_image)
        self.assertEqual(new_nodes[3].url, "http://example.com/image2.jpg")

    def test_split_nodes_image_no_images(self):
        old_nodes = [TextNode("Here is some text without images.", text_type_text)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, old_nodes)

    def test_split_nodes_link_single(self):
        old_nodes = [TextNode("Here is a link to [Google](https://www.google.com).", text_type_text)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Here is a link to ")
        self.assertEqual(new_nodes[0].text_type, text_type_text)
        self.assertEqual(new_nodes[1].text, "Google")
        self.assertEqual(new_nodes[1].text_type, text_type_link)
        self.assertEqual(new_nodes[1].url, "https://www.google.com")
        self.assertEqual(new_nodes[2].text, ".")
        self.assertEqual(new_nodes[2].text_type, text_type_text)

    def test_split_nodes_link_multiple(self):
        old_nodes = [TextNode("Link1: [Google](https://www.google.com) and Link2: [Bing](https://www.bing.com)", text_type_text)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "Link1: ")
        self.assertEqual(new_nodes[0].text_type, text_type_text)
        self.assertEqual(new_nodes[1].text, "Google")
        self.assertEqual(new_nodes[1].text_type, text_type_link)
        self.assertEqual(new_nodes[1].url, "https://www.google.com")
        self.assertEqual(new_nodes[2].text, " and Link2: ")
        self.assertEqual(new_nodes[2].text_type, text_type_text)
        self.assertEqual(new_nodes[3].text, "Bing")
        self.assertEqual(new_nodes[3].text_type, text_type_link)
        self.assertEqual(new_nodes[3].url, "https://www.bing.com")

    def test_split_nodes_link_no_links(self):
        old_nodes = [TextNode("Here is some text without links.", text_type_text)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, old_nodes)

    

if __name__ == "__main__":
    unittest.main()