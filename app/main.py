import sys
import os
import zlib


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)
    
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif command == "cat-file" and sys.argv[1] == "-p":
        file = sys.argv[3]
        obj_path = f".git/objects/{file[:2]/file[2:]}"
        with open(obj_path, "rb") as obj:
            content = obj.read
            content = zlib.decompress(content)
            content_start = content.find(b"x00")
            content = content[content_start + 1:].strip()
            print(content.decode("utf-8"), end="")
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
