from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tqdm import tqdm
from bs4 import BeautifulSoup

def extract_entries(base_url):
    """
    Extracts entries from the given base URL using Selenium and BeautifulSoup.

    Args:
        base_url (str): The base URL to start the extraction from.

    Returns:
        list: A list of dictionaries containing the extracted data.
    """
    root_url = "https://lux.collections.yale.edu"
    # Set up Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    entries = []

    # Get the total number of pages
    driver.get(base_url)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "input-group-text")))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        max_page_element = soup.find_all("span", {"class": "input-group-text"})[1]

        if max_page_element:
            max_page_text = max_page_element.text.strip()
            max_page = int(max_page_text.split()[-1])
        else:
            print("Could not find the max page element. Setting max_page to 1.")
            max_page = 1
    except:
        print("An error occurred. Assuming it's a single page.")
        max_page = 1

    for page_num in tqdm(range(1, max_page + 1)):
        page_url = f"{base_url}&ap={page_num}"

        # Load the page
        driver.get(page_url)

        # Wait for the page to load (adjust the timeout and condition as needed)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "m-2.d-flex")))

        # Allow some time for any JavaScript to execute
        time.sleep(1)

        # Get the page source after it has been rendered
        page_source = driver.page_source

        # Parse the rendered HTML with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all elements with the class "m-2 d-flex"
        items = soup.find_all(class_="m-2 d-flex")

        # Extract data from each item
        for item in items:
            entry = {}
            # Extract image URL
            img_element = item.find("img", {"class": "img-thumbnail"})
            if img_element and "src" in img_element.attrs:
                entry['image_url'] = root_url + img_element["src"]
            else:
                entry['image_url'] = None

            # Extract name and dates
            name_element = item.find("span", {"class": "sc-dmRaPn"})
            if name_element:
                name_link = name_element.find("a")
                if name_link:
                    entry['name'] = name_link.text.strip()
                    entry['link'] = root_url + name_link.get('href')

                dates_element = name_element.find("span", {"data-testid": "start-end-dates"})
                if dates_element:
                    entry['dates'] = dates_element.text.strip(', ')
                else:
                    entry['dates'] = None

            # Extract additional data
            dl_element = item.find("dl", {"class": "sc-kgflAQ"})
            if dl_element:
                dt_elements = dl_element.find_all("dt")
                dd_elements = dl_element.find_all("dd")
                for dt, dd in zip(dt_elements, dd_elements):
                    key = dt.text.strip().lower().replace('/', '_')
                    value = [a.text for a in dd.find_all("a")]
                    entry[key] = value
            # Determine the type (person or group) based on the URL
            if 'link' in entry:
                entry['type'] = 'person' if '/view/person/' in entry['link'] else 'group'
            else:
                entry['type'] = None

            entries.append(entry)

    # Don't forget to close the browser when you're done
    driver.quit()

    # Return the extracted entries
    return entries

# Example usage:
# base_url = "https://lux.collections.yale.edu/view/results/people?q=%7B%22AND%22%3A%5B%7B%22_lang%22%3A%22en%22%2C%22name%22%3A%22tolkien%22%7D%5D%7D"
# entries = extract_entries(base_url)
# print(f"Total entries extracted: {len(entries)}")
# print("Sample entry:", entries[0] if entries else "No entries found")