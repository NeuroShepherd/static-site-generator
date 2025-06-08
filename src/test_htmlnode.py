import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_repr(self):
        node = LeafNode("img", "", props={"src": "image.png", "alt": "An image"})
        self.assertEqual(node.__repr__(), "LeafNode(img, "", {'src': 'image.png', 'alt': 'An image'})")
    

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()