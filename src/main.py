import os
import shutil

from block_markdown import markdown_to_html_node


def copy_static_files():
    if os.path.exists("public"):
        shutil.rmtree("public")

    os.makedirs("public")

    queue = ["static"]

    while queue:
        current_dir = queue.pop(0)
        for file in os.listdir(current_dir):
            if os.path.isdir(os.path.join(current_dir, file)):
                queue.append(os.path.join(current_dir, file))
            else:
                target_dir = os.path.join("public", current_dir.replace("static", "").lstrip("/"))

                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                shutil.copy(os.path.join(current_dir, file), os.path.join(target_dir, file))

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.strip("#").strip()

    raise ValueError("No title found in markdown")

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using template_path {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)

    print(html_node)

    content = html_node.to_html()

    title = extract_title(markdown)

    result = template.replace("{{ Content }}", content).replace("{{ Title }}", title)

    with open(dest_path, "w") as f:
        f.write(result)

def main():
    copy_static_files()

    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
