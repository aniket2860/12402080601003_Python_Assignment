# Assignment 1
# Question 8 - Compressed Log Index using Pickle and Zip

import os
import re
import pickle
import zipfile


# Extract normalized tokens from a line
def get_tokens(line):

    return re.findall(
        r"[A-Za-z0-9_]+",
        line.lower()
    )


# Build inverted index
def build_index(folder_path):

    index = {}

    total_files = 0
    total_lines = 0

    # Scan all files in the folder
    for file_name in sorted(os.listdir(folder_path)):

        file_path = os.path.join(
            folder_path,
            file_name
        )

        if not os.path.isfile(file_path):
            continue

        total_files += 1

        try:
            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                for line_number, line in enumerate(
                    file,
                    start=1
                ):

                    total_lines += 1

                    tokens = set(
                        get_tokens(line)
                    )

                    # Add file and line to every token
                    for token in tokens:

                        if token not in index:
                            index[token] = []

                        index[token].append(
                            (file_name, line_number)
                        )

        except OSError:
            continue

    return index, total_files, total_lines


# Save index using pickle
def save_index(index, pickle_path):

    with open(
        pickle_path,
        "wb"
    ) as file:

        pickle.dump(
            index,
            file,
            protocol=pickle.HIGHEST_PROTOCOL
        )


# Create zip file
def create_zip(
    folder_path,
    pickle_path,
    zip_path
):

    with zipfile.ZipFile(
        zip_path,
        "w",
        zipfile.ZIP_DEFLATED
    ) as archive:

        # Add all log files
        for file_name in os.listdir(folder_path):

            file_path = os.path.join(
                folder_path,
                file_name
            )

            if os.path.isfile(file_path):

                archive.write(
                    file_path,
                    arcname=file_name
                )

        # Add pickle index
        archive.write(
            pickle_path,
            arcname=os.path.basename(
                pickle_path
            )
        )


# Search tokens in the index
def search_index(
    pickle_path,
    queries
):

    try:

        with open(
            pickle_path,
            "rb"
        ) as file:

            index = pickle.load(file)

    except (
        FileNotFoundError,
        pickle.PickleError,
        EOFError
    ):

        print("INVALID")
        return

    # Search every query token
    for query in queries:

        token = query.lower()

        matches = index.get(
            token,
            []
        )

        print(f"{query}:")

        for file_name, line_number in matches:

            print(
                f"{file_name}:{line_number}"
            )


# BUILD mode
def build_mode():

    parts = input().split()

    if len(parts) != 2:
        print("INVALID")
        return

    folder_path = parts[0]
    zip_path = parts[1]

    if not os.path.isdir(folder_path):
        print("INVALID")
        return

    # Create pickle file beside the zip file
    pickle_path = os.path.splitext(
        zip_path
    )[0] + ".pickle"

    index, total_files, total_lines = build_index(
        folder_path
    )

    save_index(
        index,
        pickle_path
    )

    create_zip(
        folder_path,
        pickle_path,
        zip_path
    )

    print(f"FILES {total_files}")
    print(f"LINES {total_lines}")
    print(f"TOKENS {len(index)}")


# SEARCH mode
def search_mode():

    parts = input().split()

    if len(parts) < 2:
        print("INVALID")
        return

    pickle_path = parts[0]
    queries = parts[1:]

    search_index(
        pickle_path,
        queries
    )


# Main function
def main():

    try:

        mode = input().strip().upper()

        if mode == "BUILD":

            build_mode()

        elif mode == "SEARCH":

            search_mode()

        else:

            print("INVALID")

    except KeyboardInterrupt:

        print("\nProgram stopped by user.")

    except OSError:

        print("INVALID")


# Start program
if __name__ == "__main__":
    main()