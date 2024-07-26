import unittest
from utils import text_node_to_html_node
from textnode import TextNode
from htmlnode import LeafNode

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

if __name__ == "__main__":
    unittest.main()