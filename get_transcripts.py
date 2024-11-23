from selenium import webdriver
import time
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup

def get_links(link: str, output_filename="transcript_links.txt"):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(3)
    driver.get(link)

    j = 0
    # Open the file to save links
    with open(output_filename, 'w') as file:
        while True:
            try:
                loadmore_elements = driver.find_elements(By.XPATH, "//button[contains(@class, 'e688iol0') and contains(., 'See More')]")

                if loadmore_elements and loadmore_elements[0].is_displayed():
                    button = loadmore_elements[0]

                    # Scroll to the button's position
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                    time.sleep(0.5)  # Give it a moment to adjust

                    # Wait until the button is clickable
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button)).click()
                    time.sleep(5)  # Allow time for new elements to load
                else:
                    print("No more 'See More' button to click.")
                    break
            except ElementClickInterceptedException:
                print("Element click intercepted. Trying again...")
                time.sleep(1)  # Wait a moment before retrying
                continue  # Retry the loop to try clicking again
            except (StaleElementReferenceException, NoSuchElementException) as e:
                print(f"Exception occurred: {e}")
                break

            # Collect links after clicking 'See More'
            t_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/#transcription')]")
            newlist = t_links[j:]  # Get new links since last collected
            if newlist:
                print(f"Found {len(newlist)} new links.")
                for link in newlist:
                    link_url = link.get_attribute('href')
                    print(link_url)
                    file.write(link_url + "\n")  # Save to file
            else:
                print("No new links found.")
            
            j = len(t_links)  # Update index for next iteration

    driver.quit()


def get_transcription(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        transcriptions = soup.find_all('span', class_='podcast-transcription-text')

        transcription_text = ' '.join([text.get_text() for text in transcriptions])

        return transcription_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def process_links_from_file(filename):
    with open(filename, 'r') as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip() 
        print(f"Processing {url}...")

        transcription = get_transcription(url)

        if transcription:
            print(f"collected transcription for {url}:")

            with open("transcriptions.txt", 'a') as output_file:
                output_file.write(f"Transcription for {url}:\n")
                output_file.write(transcription + "\n\n")
        else:
            print(f"Failed to fetch transcription for {url}.")


def complete_task(start_url, links_file="transcript_links.txt"):
    # Step 1: Get links and save them to a file
    get_links(start_url, links_file)

    # Step 2: Process the links from the saved file
    process_links_from_file(links_file)


# Example usage:
# Start the process with the initial URL.
# This will fetch the links, save them to a file, and then process those links.
start_url = "https://www.iheart.com/podcast/1119-the-bobby-bones-show-25100459/"
complete_task(start_url)
