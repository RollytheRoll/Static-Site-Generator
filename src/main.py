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
    from_path = "./content"
    template_path = "./template.html"
    dest_path = "./public"
    generate_page_recursive(from_path, template_path, dest_path)


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
    dest_path, _ = os.path.splitext(dest_path)
    dest_path = dest_path + ".html"
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
    if not os.path.exists(os.path.dirname(dest_path)):
        os.mkdir(os.path.dirname(dest_path))
    
    html = open(dest_path,"w")
    html.write(template_file)
    html.close()

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    paths = dir_path_content
    if os.path.isdir(paths):
        paths = os.listdir(paths)
    for path in paths:
        new_path = os.path.join(dir_path_content,path)
        if os.path.isfile(new_path):
            generate_page(new_path,template_path,os.path.join(dest_dir_path,path))
            continue
        if os.path.isdir(new_path):
            os.mkdir(os.path.join(dest_dir_path, path))
            generate_page_recursive(new_path,template_path,os.path.join(dest_dir_path, path))


main() 

