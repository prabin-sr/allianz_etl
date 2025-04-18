# Alliance ETL Task
HTTP requests, HTML Parsing, grouping and aggregation of datasets, ZipFile processing and Excel Workbooks generation.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Installation and Usage Instructions

## Installation

1.  **Install Python 3.13:**

    * Ensure you have Python 3.13 installed on your system. You can download it from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
    * Verify the installation by opening a terminal or command prompt and typing:
        ```bash
        python --version
        ```
        or
        ```bash
        python3 --version
        ```
        The output should display "Python 3.13.x" (where x is the minor version number).

2.  **Install Requirements:**

    * Navigate to the directory containing the `requirements.txt` file.
    * Install the required Python packages using pip:
        ```bash
        pip install -r requirements.txt
        ```

## Usage

1.  **Navigate to the `src` Directory:**

    * Open a terminal or command prompt and change the current directory to the `src` directory:
        ```bash
        cd src
        ```

2.  **Run the Main Script:**

    * Execute the `main.py` script:
        ```bash
        python main.py
        ```

3.  **Output:**

    * The script will create a folder named `media` under the `src` directory.
    * The `media` folder will contain the generated zip file and the excel file.

## Running Tests

1.  **Navigate to the `src` Directory (if you are not already there):**
    ```bash
    cd src
    ```
2.  **Run Tests:**

    * To run the tests, use the following command:
        ```bash
        pytest
        ```
    * To run the tests and see the print statements, use the following command:
        ```bash
        pytest -s
        ```
        The `-s` flag prevents pytest from capturing the output, allowing you to see any `print()` statements in your code.
