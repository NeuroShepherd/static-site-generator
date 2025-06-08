import unittest
from htmlnode import HTMLNode, LeafNode

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


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "Inline text", {"class": "inline"})
        self.assertEqual(node.to_html(), '<span class="inline">Inline text</span>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(value="Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("div")
            
    def test_leaf_no_value_with_tag(self):
        with self.assertRaises(ValueError):
            LeafNode("div", None)
    

if __name__ == "__main__":
    unittest.main()