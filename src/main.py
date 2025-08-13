import sys

from helperfunctions import copy_from_dir_to_dir, generate_page_recursive

def main():
    if len(sys.argv) != 2:
        base_path = "/"
    else:
        base_path = sys.argv[1]
    if not base_path.endswith("/"):
        base_path += "/"
    print(f"[DEBUG] base_path: '{base_path}'")
    copy_from_dir_to_dir("./static", "./docs")
    generate_page_recursive("./content", "./template.html", "./docs", base_path)


if __name__ == "__main__":
    main()