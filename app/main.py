import sys
import os
import zlib
import hashlib

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

    elif command == "cat-file" and sys.argv[2] == "-p":
        file = sys.argv[3]
        obj_path = f".git/objects/{file[:2]}/{file[2:]}"
        with open(obj_path, "rb") as obj:
            content = obj.read()
            content = zlib.decompress(content)
            content_start = content.find(b"\x00")
            content = content[content_start + 1:].strip()
            print(content.decode("utf-8"), end="")
    
    elif command == "hash-object" and sys.argv[2] == "-w":
        file = sys.argv[3]
        with open(file, "rb") as f:
            content = f.read()
        
        header = f"blob {len(content)}\0".encode("utf-8")
        store = header + content

        hashed_object = hashlib.sha1(store).hexdigest()
        print(hashed_object)

        dir_name = f".git/objects/{hashed_object[:2]}"
        file_name = hashed_object[2:]
        os.makedirs(dir_name)
        object_path = f"{dir_name}/{file_name}"

        with open(object_path, "wb") as object:
            object.write(zlib.compress(store))
    
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
