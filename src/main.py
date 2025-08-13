import os

from helperfunctions import copy_from_dir_to_dir, generate_page_recursive

def main():
    copy_from_dir_to_dir("./static", "./public")
    generate_page_recursive("./content", "./template.html", "./public")


if __name__ == "__main__":
    main()