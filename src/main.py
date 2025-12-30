import os
import shutil

from textnode import TextType, TextNode


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

def main():
    copy_static_files()


if __name__ == "__main__":
    main()
