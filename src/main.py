import os
import shutil
import sys

from block_markdown import markdown_to_html_node


def copy_static_files(target_dir: str):
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    os.makedirs(target_dir)

    queue = ["static"]

    while queue:
        current_dir = queue.pop(0)
        for file in os.listdir(current_dir):
            if os.path.isdir(os.path.join(current_dir, file)):
                queue.append(os.path.join(current_dir, file))
            else:
                final_target_dir = os.path.join(target_dir, current_dir.replace("static", "").lstrip("/"))

                if not os.path.exists(final_target_dir):
                    os.makedirs(final_target_dir)

                shutil.copy(os.path.join(current_dir, file), os.path.join(final_target_dir, file))

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.strip("#").strip()

    raise ValueError("No title found in markdown")

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)

    content = html_node.to_html()

    title = extract_title(markdown)

    result = template.replace("{{ Content }}", content).replace("{{ Title }}", title).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    with open(dest_path, "w") as f:
        f.write(result)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str):
    queue = [dir_path_content]

    while queue:
        current_dir = queue.pop(0)
        for file in os.listdir(current_dir):
            if os.path.isdir(os.path.join(current_dir, file)):
                queue.append(os.path.join(current_dir, file))
            else:
                if file.endswith(".md"):
                    file_path = os.path.join(current_dir.replace(dir_path_content, "").lstrip("/"), file.replace(".md", ".html"))
                    target_path = os.path.join(dest_dir_path, file_path)
                    parent_dir = os.path.dirname(target_path)
                    if not os.path.exists(parent_dir):
                        os.makedirs(parent_dir)
                    generate_page(os.path.join(current_dir, file), template_path, target_path, basepath)

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_static_files("docs")

    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
