# Yale Lux Search Overlap Identifier

This project is designed to take in a Yale Lux Search URL and identify potentially overlapping records. The main script, `separate.py`, downloads entries from the given URL, processes them to clean and standardize the data, and then creates a hierarchical tree structure to visualize the relationships between the entries.

## Features

- Downloads entries from a given Yale Lux Search URL using Selenium and BeautifulSoup.
- Cleans and standardizes the data, including handling parentheticals, abbreviations, and name parts.
- Creates a hierarchical tree structure to visualize the relationships between the entries.
- Outputs the tree structure to a specified file.

## Requirements

- Python 3.6+
- Selenium
- BeautifulSoup4
- tqdm
- anytree
- nameparser

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/wjbmattingly/yale-lux-overlap
    cd yale-lux-overlap
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Set up Selenium and ChromeDriver:

    ### Windows

    - Download the ChromeDriver from [here](https://developer.chrome.com/docs/chromedriver/downloads).
    - Extract the downloaded file and place it in a directory of your choice.
    - Add the directory containing `chromedriver.exe` to your system's PATH environment variable.

    ### macOS

    - Install ChromeDriver using Homebrew:

        ```sh
        brew install chromedriver
        ```

    ### Linux

    - Download the ChromeDriver from [here](https://developer.chrome.com/docs/chromedriver/downloads).
    - Extract the downloaded file and place it in a directory of your choice.
    - Add the directory containing `chromedriver` to your system's PATH environment variable.

## Usage

To use the script, run the following command:

```sh
python separate.py <url> [output]
```

- `<url>`: The Yale Lux Search URL to process.
- `[output]`: (Optional) The output file to save the tree structure. Defaults to `output.txt`.

### Example

```sh
python separate.py "https://lux.collections.yale.edu/view/results/people?q=%7B%22AND%22%3A%5B%7B%22_lang%22%3A%22en%22%2C%22name%22%3A%22tolkien%22%7D%5D%7D" output.txt
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
