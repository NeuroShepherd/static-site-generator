import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("div", "Hello, World!", [], {"class": "greeting"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello, World!")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "greeting"})

    def test_props_to_html(self):
        node = HTMLNode("span", "Text", props={"style": "color: red;"})
        self.assertEqual(node.props_to_html(), ' style="color: red;"')

    def test_repr(self):
        node = HTMLNode("p", "Paragraph", [], {"id": "main"})
        self.assertEqual(repr(node), "HTMLNode(TAG=p, VALUE=Paragraph, CHILDREN=[], PROPS={'id': 'main'})")

if __name__ == "__main__":
    unittest.main()