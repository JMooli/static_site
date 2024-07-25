import unittest

from htmlnode import HTMLnode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestTextNode(unittest.TestCase):
    def test_leaf_node(self):
        leaf = LeafNode("b", "Bold text")
        self.assertEqual(leaf.to_html(), "<b>Bold text</b>")

    def test_leaf_node_no_tag(self):
        leaf = LeafNode(value="Plain text")
        self.assertEqual(leaf.to_html(), "Plain text")

    def test_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"class": "container"}
        )
        self.assertEqual(node.to_html(), '<p class="container"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_parent_node_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", [])


if __name__ == "__main__":
    unittest.main()
