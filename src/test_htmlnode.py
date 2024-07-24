import unittest

from htmlnode import HTMLnode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLnode(tag= "p", props={"p": "container"})
        node2 = HTMLnode(tag= "div", props={"div": "container"})
        node3 = HTMLnode(tag= "link", props={"href": "www.google.com"})
        print(node)
        print(node2)
        print(node3)
        print(node3.props_to_html())

if __name__ == "__main__":
    unittest.main()
