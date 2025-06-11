from textnode import TextNode, TextType
from helpers import (
    source_to_dest,
    generate_page,
    generate_pages_recursive,
)
import os, sys, shutil

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"

def main():
    # text_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    # print(text_node.__repr__())
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    source_to_dest(dir_path_static, dir_path_public)
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)

if __name__ == "__main__":
    main()
