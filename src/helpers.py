from htmlnode import LeafNode, ParentNode
from textnode import TextType, TextNode
# from blocktype import block_to_block_type
import re, os, shutil
from enum import Enum





class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_block_type(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)














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


def text_to_textnodes(text):
    """
    Converts a raw string of markdown-flavored text into a list of TextNode objects.
    """
    nodes = [TextNode(text, TextType.TEXT)]
    # Split links
    nodes = split_nodes_link(nodes)
    # Split images
    nodes = split_nodes_image(nodes)
    # Split bold text
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    # Split italic text
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    # Split code blocks
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes


def markdown_to_blocks(markdown):
    splitty_bois = markdown.split("\n\n")
    lines_stripped = []
    for boi in splitty_bois:
        stripped = boi.strip()
        if stripped:
            lines_stripped.append(stripped)
    return lines_stripped



def source_to_dest(source_dir, dest_dir):
    # delete old
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir, exist_ok=True)

    for item in os.listdir(source_dir):
        src_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isdir(src_path):
            source_to_dest(src_path, dest_path)  # Recursive call for subdirectories
        else:
            shutil.copy2(src_path, dest_path)
            print(f"Copied: {src_path} -> {dest_path}")
    


def extract_title(markdown):
    """
    Extracts the title from a markdown string.
    The title is assumed to be the first line of the markdown.
    """
    lines = markdown.split("\n")
    title_lines = []
    for line in lines:
        if line.startswith("# "):
            title_lines.append(line.strip("# ").strip())
    if len(title_lines) == 0:
        raise Exception("No title found in markdown")
    return title_lines.pop(0) # the .pop method can be removed to return all titles, but we only want the first one
    


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as temp:
        template = temp.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    result = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    # now write the result as a new file with any necessary directories to the dest_path
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as out:
        out.write(result)


def clear_public_dir():
    public_dir = "public"
    if os.path.exists(public_dir):
        for item in os.listdir(public_dir):
            item_path = os.path.join(public_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    """
    Recursively generates pages from markdown files in the given directory.
    """
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            # Compute the corresponding subdirectory in the destination
            sub_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, sub_dest_dir, basepath)
        elif item.endswith(".md"):
            # Compute the relative path from the content root
            rel_path = os.path.relpath(item_path, dir_path_content)
            # Remove .md extension and add .html
            html_filename = os.path.splitext(item)[0] + ".html"
            # Compute the destination path, preserving subfolders
            dest_path = os.path.join(dest_dir_path, html_filename)
            generate_page(item_path, template_path, dest_path, basepath)