import os
import shutil
from markdown_blocks import *
from htmlnode import *
from markdown import *
from textnode import *

def main():
    if os.path.exists("./public/"):
        shutil.rmtree("./public/")
    os.mkdir("./public")
    paths = os.listdir("./src/static")
    parent_path = "./src/static"
    dst_path = "./public"
    copy_static_to_public(paths, parent_path, dst_path)
    from_path = "./content/index.md"
    template_path = "./template.html"
    dest_path = "./public/index.html"
    generate_page(from_path, template_path, dest_path)


def copy_static_to_public(paths, parent_path, dst_path):
    if len(paths) == 0:
        return None

    for path in paths:
        new_path = os.path.join(parent_path, path)
        if os.path.isfile(new_path):
            shutil.copy(new_path, dst_path)
            return copy_static_to_public(paths[1:], parent_path, dst_path)
        if os.path.isdir(new_path):
            new_dst_path = os.path.join(dst_path,path)
            new_parent_path = os.path.join(parent_path,path)
            os.mkdir(new_dst_path)
            return copy_static_to_public(os.listdir(new_path),new_parent_path,new_dst_path), copy_static_to_public(paths[1:],parent_path,dst_path)
        
def extract_title(markdown):
    for line in markdown:
        if line.startswith("#"):
            return line.lstrip("#").strip()
        
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path)
    markdown_file = markdown.read()
    markdown.close()
    template = open(template_path)
    template_file = template.read()
    template.close()
    content = markdown_to_html_node(markdown_file).to_html()
    title = extract_title(markdown_file)
    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", content)
    html = open(dest_path,"w")
    html.write(template_file)
    html.close()

main() 

