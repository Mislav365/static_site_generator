import os
import shutil

from markdownparser import markdown_to_html_node


def copy_from_dir_to_dir(from_dir, to_dir):
    if os.path.exists(to_dir):
        shutil.rmtree(to_dir)
    os.mkdir(to_dir)
    if not os.path.exists(from_dir):
        raise FileNotFoundError(f"The source directory '{from_dir}' does not exist.")
    files_to_copy = os.listdir(from_dir)
    for file_name in files_to_copy:
        full_file_name = os.path.join(from_dir, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, to_dir)
        elif os.path.isdir(full_file_name):
            copy_from_dir_to_dir(full_file_name, os.path.join(to_dir, file_name))

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found in the markdown content.")

def generate_page(from_path, template_path, dest_path, base_path):
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"The source file '{from_path}' does not exist.")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"The template file '{template_path}' does not exist.")
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    print(f"Generating page from {from_path} to {dest_path} using {template_path} ")
    with open(from_path, 'r') as f:
        content = f.read()

    with open(template_path, 'r') as f:
        template = f.read()

    html_node = markdown_to_html_node(content)
    html_rendered = html_node.to_html()
    title = extract_title(content)
    page_content = template.replace("{{ Title }}", title).replace("{{ Content }}", html_rendered)

    page_content = page_content.replace('href="/', f'href="{base_path}')
    page_content = page_content.replace('src="/', f'src="{base_path}')

    with open(dest_path, 'w') as f:
        f.write(page_content)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path, base_path="/"):
    if os.path.isdir(dir_path_content):
        for item in os.listdir(dir_path_content):
            item_path = os.path.join(dir_path_content, item)
            if os.path.isdir(item_path):
                generate_page_recursive(item_path, template_path, os.path.join(dest_dir_path, item), base_path)
            elif item.endswith('.md'):
                dest_path = os.path.join(dest_dir_path, item.replace('.md', '.html'))
                generate_page(item_path, template_path, dest_path, base_path)