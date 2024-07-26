import unittest
from textnode import TextNode, text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image
from utils import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_text_type_bold(self):
        text = "This is start** bold ** end."
        delimiter = "**"
        result = split_nodes_delimiter(text, delimiter, text_type_bold)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is start")
        self.assertEqual(result[0].text_type, text_type_text)
        self.assertEqual(result[1].text, " bold ")
        self.assertEqual(result[1].text_type, text_type_bold)
        self.assertEqual(result[2].text, " end.")
        self.assertEqual(result[2].text_type, text_type_text)

    def test_split_text_type_italic(self):
        text = "This is beginnign *text1, This is italic* and here it ends"
        delimiter = "*"
        result = split_nodes_delimiter(text, delimiter, text_type_italic)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is beginnign ")
        self.assertEqual(result[0].text_type, text_type_text)
        self.assertEqual(result[1].text, "text1, This is italic")
        self.assertEqual(result[1].text_type, text_type_italic)
        self.assertEqual(result[2].text, " and here it ends")
        self.assertEqual(result[2].text_type, text_type_text)

    def test_split_text_type_code(self):
        text = "start `code` test"
        delimiter = "`"
        result = split_nodes_delimiter(text, delimiter, text_type_code)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "start ")
        self.assertEqual(result[0].text_type, text_type_text)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, text_type_code)
        self.assertEqual(result[2].text, " test")
        self.assertEqual(result[2].text_type, text_type_text)

    def test_split_unsupported_text_type(self):
        text = "unsupported text1.unsupported text2"
        delimiter = "."
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(text, delimiter, "unsupported")
        self.assertTrue("unsupported text type: unsupported" in str(context.exception))

if __name__ == "__main__":
    unittest.main()
