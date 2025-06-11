print("hello world")
from textnode import TextNode, TextType
from helpers import (
    source_to_dest,
    generate_page,
    clear_public_dir,
    generate_pages_recursive,
)
import os

def main():
    # text_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    # print(text_node.__repr__())
    clear_public_dir()
    source_to_dest("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
