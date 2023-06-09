# :file_folder:  File Difference Checker

**:file_folder: File Difference Checker** is a Python script that allows you to compare the contents of two text files and identify the differences between them. It provides a convenient way to analyze and understand changes between two versions of a file.

## :sparkles: Features

-   **Main:**
    -   Compare two text files and identify the lines that differ
    -   Integrate with **_Ansible/YAML_** for automated file difference checking
-   **Other:**
    -   Handle exceptions for specific lines that should be excluded from the comparison
    -   Filter out empty lines and remove newline characters for accurate comparison
    -   Display differences with line numbers and file references for easy reference
    -   Calculate the similarity percentage between the files

### :computer: Tested Platforms

-   Linux (Tested ✔️)
-   Windows (Tested ✔️)
-   MacOS (Not Tested ❌)

## :link: Dependencies

To run this project, you need to have the following dependencies installed:

-   🐍 [Python](https://www.python.org/downloads/): Python is a programming language used by this project.
-   📦 [pip](https://pip.pypa.io/en/stable/): pip is the package installer for Python.

## :inbox_tray: Installation

<!-- ##### Debian-based (e.g., Ubuntu, Debian): -->
<!-- ##### RPM-based (e.g., Fedora, CentOS, Red Hat Enterprise Linux): -->
<!-- ##### Windows -->

Clone the repository to your directory

```xml
cd <directory>
git clone <repository_url>
```



## :hammer_and_wrench: Usage

Execute **[compare.py](./compare.py)** script with specified arguments

##### Linux

```xml
python3 compare.py --file1 <file_1> --file2 <file_2>
```
or
```xml
python3 compare.py --file1 <file_1> --file2 <file_2> --exceptions <exception_1> <exception_2>
```
##### Windows

```xml
python compare.py --file1 <file_1> --file2 <file_2>
```
or
```xml
python compare.py --file1 <file_1> --file2 <file_2> --exceptions <exception_1> <exception_2>
```

## :wrench: Integration

The File Difference Checker can be easily integrated with YAML configurations, such as in Ansible playbooks, to automate the process of file comparison. Here's an example of how you can integrate the script with YAML:

1. Create an Ansible playbook or YAML configuration file.

2. Define the playbook tasks to include the **[File Difference Checker script](./file_difference_checker.yaml)**.

```yaml
---
- name: File Difference Checker # Playbook name
  hosts: localhost # Target host
  gather_facts: false # Disable gathering facts about the host

  vars:
      exceptions: # List of exceptions
          - SERVER
          - ID
          - PASSWORD

  tasks:
      - name: Exceptions Specification # Task to display exceptions
        debug:
            msg: "{{ exceptions | to_json }}"

      - name: Run script # Task to run the script
        shell: "python3 compare.py --file1 <FILE 1> --file2 <FILE 2> --exceptions {{ exceptions | to_json }}"
        register: cmd_output # Register the output of the command

      - name: Get output # Task to display the command output
        debug:
            var: cmd_output.stdout_lines
```

## :page_with_curl: Examples

Here are some examples to illustrate how the File Difference Checker works and what it returns:

**Example 1**: Identical Files

```shell
$ python3 compare.py --file1 file1.txt --file2 file2.txt
```

Output:

```shell
Comparing file1.txt and file2.txt
------ There are no exceptions 

No differences found

```

**Example 2: Different Files (without exceptions)**

_file1.txt_

```python
def testMessage(message: str):
    print(message)

testMessage('Hello World')
```

_file2.txt_

```python
def testMessage(text: str):
    print(text)

testMessage('Hello World')
```

---

```shell
$ python3 compare.py --file1 file1.txt --file2 file2.txt
```

Output:

```shell

Comparing file1.txt and file2.txt
------ There are no exceptions 

The difference N-0:
 File file1.txt: In < def testMessage(message: str): > 
 File file2.txt: In < def testMessage(text: str): >

The difference N-1:
 File file1.txt: In < print(message) > 
 File file2.txt: In < print(text) >

Total Differences Found: 2
Files equal: 33.33%

```

**Example 3: Different Files (with exceptions)**

_file1.txt_

```python
import logging as log
import numpy as num
import cv2 as cv

image_2 = cv.imread("assets/2.png")


def testMessage(message: str):
    print(message)


testMessage('Hello World')

```

_file2.txt_

```python
import logging
import numpy as np
import cv2

image_5 = cv2.imread('assets/5.png')


def testMessage(text: str):
    print(text)


testMessage('Hello World')

```

---

```shell
$ python3 compare.py --file1 file1.txt --file2 file2.txt --exceptions import image
```
Output:
```shell

Comparing test-1.py and test-2.py
------ Exceptions: ['import', 'image'] 

------ EXCEPTION: import logging as log 
 import logging 

------ EXCEPTION: import numpy as num 
 import numpy as np 

------ EXCEPTION: import cv2 as cv 
 import cv2 

------ EXCEPTION: image_2 = cv.imread("assets/2.png") 
 image_5 = cv2.imread('assets/5.png') 

The difference N-4:
 File file1.txt: In < def testMessage(message: str): > 
 File file2.txt: In < def testMessage(text: str): >

The difference N-5:
 File file1.txt: In < print(message) > 
 File file2.txt: In < print(text) >

Total Differences Found: 2
Files equal: 14.29%

```
In this example, the File Difference Checker compares _file1.txt_ and _file2.txt_. The script identifies differences after excluding the lines **starting** with *"import"* and *"image"* due to the specified exceptions.

## :page_with_curl: Code Description

The code provided is a Python script for comparing the contents of two files and identifying the differences between them. It uses the `argparse` module to parse command-line arguments, allowing users to specify the paths to the two files to be compared. Additionally, users can provide a list of exception lines that will be ignored during the comparison.

The main function in the code is `differ`, which takes two file paths as input parameters and returns the differences found between the files. The function follows these steps:

1. It reads the lines from both files and filters out newline characters.
2. Empty lines are removed from the filtered lines.
3. The filtered lines of each file are compared to check for identical contents. If the files are identical, the function returns "No differences found."
4. If the filtered lines differ, the function proceeds to compare line by line, identifying differences and accounting for the specified exceptions. Differences are printed along with the corresponding line numbers (line number is considered to be the line number of a filtered file) and files.
5. If the number of lines in the files is not equal, the function handles the case and prints the line from the file with more lines.
6. After comparing all lines, the function displays the total number of differences found.
7. Finally, the function calculates the file similarity percentage using the `difflib.SequenceMatcher` and returns the result.

The script also includes an `if __name__ == "__main__":` block, which handles the command-line arguments using `argparse`. It calls the `differ` function with the provided file paths and exceptions, and prints the output.

The code provides flexibility for customization through the use of variables such as `allowLogs` (for enabling or disabling logs (which are basically additional lines of data )), `exceptions` (for specifying exception keywords), and command-line arguments.

The code can be integrated with other tools or workflows, such as Ansible/YAML, by invoking the script with appropriate arguments and capturing the output for further processing.


## :raising_hand: Contributing

🙌 Contributions to this project are welcome! If you have any ideas, improvements, or bug fixes, please submit a pull request 🛠️. For major changes, please open an issue to discuss your ideas beforehand 💡.

## :scroll: License

This project is licensed under the MIT License 📜.

## :pray: Acknowledgments
Special thanks to @diniliaqil for the inspiration and idea behind this project. Your contribution is greatly appreciated.
