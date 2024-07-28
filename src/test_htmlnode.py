import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

class TestParentNode(unittest.TestCase):
    def test_parent_node_initialization(self):
        child = LeafNode('p', 'Hello, World!')
        parent = ParentNode('div', [child])
        self.assertEqual(parent.tag, 'div')
        self.assertEqual(parent.children, [child])
        self.assertEqual(parent.props, None)

    def test_parent_node_to_html_without_tag(self):
        child = LeafNode('p', 'Hello, World!')
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: no tag")

    def test_parent_node_to_html_without_children(self):
        parent = ParentNode('div', None)
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: no children")

    def test_parent_node_to_html(self):
        child1 = LeafNode('p', 'Hello, World!')
        child2 = LeafNode('span', 'This is a test.')
        parent = ParentNode('div', [child1, child2])
        self.assertEqual(parent.to_html(), '<div><p>Hello, World!</p><span>This is a test.</span></div>')

    def test_parent_node_with_props(self):
        child1 = LeafNode('p', 'Hello, World!')
        child2 = LeafNode('span', 'This is a test.')
        parent = ParentNode('div', [child1, child2], props={'class': 'container', 'id': 'main'})
        self.assertEqual(parent.to_html(), '<div class="container" id="main"><p>Hello, World!</p><span>This is a test.</span></div>')

    def test_repr(self):
        child1 = LeafNode('p', 'Hello, World!')
        parent = ParentNode('div', [child1], props={'class': 'container'})
        self.assertEqual(repr(parent), "ParentNode(div, children: [LeafNode(p, Hello, World!, None)], {'class': 'container'})")

if __name__ == "__main__":
    unittest.main()
