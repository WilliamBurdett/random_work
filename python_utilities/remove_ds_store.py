import os
import sys


def main():
    root_path = sys.argv[1]
    for root, dirs, files in os.walk(root_path):
        for file in files:
            path = os.path.join(root, file)
            if path.endswith(".DS_Store"):
                print(f"Found: {path} - removing")
                os.remove(path)


if __name__ == '__main__':
    main()
