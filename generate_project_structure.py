# generate_project_structure.py

import os

def generate_folder_tree(root_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            level = dirpath.replace(root_dir, '').count(os.sep)
            indent = '│   ' * level
            f.write(f"{indent}├── {os.path.basename(dirpath)}/\n")
            subindent = '│   ' * (level + 1)
            for filename in filenames:
                f.write(f"{subindent}└── {filename}\n")

if __name__ == "__main__":
    ROOT_DIR = os.path.abspath(".")  # or provide a path
    OUTPUT_FILE = "project_structure.txt"
    generate_folder_tree(ROOT_DIR, OUTPUT_FILE)
    print(f"✅ Folder structure saved to: {OUTPUT_FILE}")
