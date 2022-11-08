import os
import sys


def replace_tabs(file_path: str):
    print(f"Checking File {file_path}")
    with open(file_path, "r") as f:
        input_text = f.read()
    if "\t" in input_text:
        print(f"Fixing File {file_path}")
        output_text = input_text.replace("\t", "    ")
        with open(file_path, "w") as f:
            f.write(output_text)


def main():
    root_path = sys.argv[1]
    for root, dirs, files in os.walk(root_path):
        for file in files:
            path = os.path.join(root, file)
            if path.endswith(".gd"):
                if r"\my-rogue\venv" not in path:
                    replace_tabs(path)


if __name__ == '__main__':
    main()
