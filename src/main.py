print("hello world")
from textnode import TextNode, TextType

def main():
    text_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(text_node.__repr__())

if __name__ == "__main__":
    main()
