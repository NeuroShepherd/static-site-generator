from htmlnode import LeafNode
from textnode import TextType, TextNode
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unknown text type: {text_node.text_type}")
        

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
            
        

def extract_markdown_images(text):
    """
    Extracts image URLs from markdown image syntax in the given text.
    Returns a list of tuples. Each tuple should contain the alt text 
    and the URL of any markdown images. For example:
    """
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return [(alt_text, url) for alt_text, url in matches]



def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        sections = extract_markdown_images(old_node.text)
        if not sections:
            new_nodes.append(old_node)
            continue
        for alt_text, url in sections:
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
    return new_nodes



def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        sections = re.split(r'\[(.*?)\]\((.*?)\)', old_node.text)
        if len(sections) % 3 != 1:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(0, len(sections), 3):
            if sections[i] != "":
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            if i + 1 < len(sections) and sections[i + 1] != "":
                new_nodes.append(TextNode(sections[i + 1], TextType.LINK, sections[i + 2]))
    return new_nodes


node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)
new_nodes = split_nodes_link([node])
print(new_nodes)