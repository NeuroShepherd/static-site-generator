print("hello world")
from textnode import TextNode, TextType
from helpers import source_to_dest

def main():
    text_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(text_node.__repr__())
    source_to_dest("static", "public")

if __name__ == "__main__":
    main()
