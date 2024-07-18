import os
import re
from collections import Counter
import time
import argparse
import math

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def find_file(filename, start_dir):
    if not re.match(r"^[a-zA-Z0-9_.\- ()]*$", filename):
        print("Invalid filename. Filenames can contain alphanumeric characters, underscores, periods, hyphens, parentheses, and spaces.")
        return

    print("Processing... Please wait.")
    try:
        for root, dirs, files in os.walk(start_dir):
            if filename in files:
                return os.path.join(root, filename)
    except PermissionError:
        pass

    return None

def count_files_and_bytes(start_dir):
    total_files = 0
    total_bytes = 0
    extension_counter = Counter()

    print("Processing... Please wait.")
    try:
        for root, dirs, files in os.walk(start_dir):
            total_files += len(files)
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    total_bytes += os.path.getsize(filepath)
                except FileNotFoundError:
                    pass
                _, extension = os.path.splitext(file)
                extension_counter[extension.lower()] += 1 
    except PermissionError:
        pass 

    return total_files, total_bytes, extension_counter

def main():
    parser = argparse.ArgumentParser(description='File operations')
    parser.add_argument('--filename', type=str, help='Filename to search')
    parser.add_argument('--start_dir', type=str, default='/', help='Directory to start the search')
    args = parser.parse_args()

    while True:
        print("\n1. Find a file")
        print("2. Count files and display summary information")
        print("3. Exit")
        choice = input("Please enter the number corresponding to your choice: ")

        if choice == "1":
            filename = args.filename if args.filename else input("Enter the filename to search: ")
            start_time = time.time()
            file_location = find_file(filename, args.start_dir)
            end_time = time.time()
            if file_location:
                print(f"File found at: {file_location}")
            else:
                print(f"{filename} not found.")
            print(f"Time taken: {end_time - start_time} seconds")
        elif choice == "2":
            start_time = time.time()
            total_files, total_bytes, extensions_counted = count_files_and_bytes(args.start_dir)
            end_time = time.time()
            print(f"Total Files: {total_files}")
            print(f"Total Bytes Used: {convert_size(total_bytes)}")
            for extn,count in extensions_counted.items():
                print(f"{extn}: {count} files")
            print(f"Time taken: {end_time - start_time} seconds")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
