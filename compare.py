import argparse
import re
import difflib
import sys

allowLogs = True  # Set this variable to True or False as needed

# Exceptions: Specify the keywords that the statements in your code start with.
# For example, if a statement in your code is "server_id = 103", you can specify "server_id" as an exception.
exceptions = []

# Display additional info about data processing


def log_print(*args):
    if allowLogs:
        print("------", *args, '\n')

# Remove newline characters from the line


def filterLine(line: str):
    filteredLine = re.sub(r"(\n|\\n|\r)+", "", line)
    return filteredLine.strip()

# Filter out empty strings from the list


def filterList(lst: list):
    filteredList = [line for line in lst if line != ""]
    return filteredList

# Checks whether line starts with exception keyword


def isLineHaveException(line: str):
    if exceptions:
        for excp in exceptions:
            if line.startswith(excp):
                return True
    return False

# Compare the contents of two files


def differ(file1, file2):
    global exceptions

    print(f"\nComparing {file1} and {file2}")

    if file_exceptions:
        exceptions = [excp.strip('[').strip(',').strip(']')
                      for excp in file_exceptions]
        log_print(f"Exceptions: {exceptions}")
    else:
        log_print('There are no exceptions')

    try:
        # Attempt to open the files
        with open(file1_path, 'r') as firstFile, open(file2_path, 'r') as secondFile:
            # Read the lines from the files
            raw_file1_lines = firstFile.readlines()
            raw_file2_lines = secondFile.readlines()

    except FileNotFoundError as e:
        log_print(f"Error: {e}")
        sys.exit(1)  # Terminate the script with a non-zero exit code

    # Check if the files are identical
    if raw_file1_lines == raw_file2_lines:
        return "No differences found\n"

    # Filter the lines in each file
    filtered_file1_lines = [filterLine(line) for line in raw_file1_lines]
    filtered_file2_lines = [filterLine(line) for line in raw_file2_lines]

    # Filter out empty lines
    filtered_file1_lines = filterList(filtered_file1_lines)
    filtered_file2_lines = filterList(filtered_file2_lines)

    # Check if the filtered files are identical
    if filtered_file1_lines == filtered_file2_lines:
        return "No differences found\n"

    # Find the differences between the files
    maxLines = max(len(filtered_file1_lines), len(filtered_file2_lines))
    lineCounter = 0
    totalDifferences = 0

    while lineCounter < maxLines:
        try:
            file1_line = filtered_file1_lines[lineCounter]
            file2_line = filtered_file2_lines[lineCounter]

            if file1_line != file2_line:
                # Check for exceptions
                if isLineHaveException(file1_line) and isLineHaveException(file2_line):
                    log_print('EXCEPTION:', file1_line, '\n', file2_line)
                else:
                    print(
                        f'The difference N-{lineCounter}:\n File {file1}: In < {file1_line} > \n File {file2}: In < {file2_line} >\n')

                    totalDifferences += 1

        except IndexError:
            # If the line numbers are not equal
            moreLineFile = filtered_file1_lines if len(
                filtered_file1_lines) == maxLines else filtered_file2_lines

            larger_file = file1 if moreLineFile == filtered_file1_lines else file2
            print(
                f'Only file {larger_file} has: < {moreLineFile[lineCounter]} >\n')
            totalDifferences += 1

        lineCounter += 1

    print(f"Total Differences Found: {totalDifferences}")

    # Return difference percentage
    matcher = difflib.SequenceMatcher(
        None, filtered_file1_lines, filtered_file2_lines)
    fileSimilarity = round(matcher.ratio() * 100, 2)
    return f"Files equal: {fileSimilarity}%"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two files.")
    parser.add_argument(
        "--file1", help="Path to the first file", required=True)
    parser.add_argument(
        "--file2", help="Path to the second file", required=True)
    parser.add_argument(
        "--exceptions",
        nargs="*",
        help=("Exception lines that are not counted")
    )
    args = parser.parse_args()

    file1_path = args.file1
    file2_path = args.file2
    file_exceptions = args.exceptions

    try:
        print(differ(file1_path, file2_path))
    except Exception as e:
        print(f"An error occurred: {e}")
