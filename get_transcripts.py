from selenium import webdriver
import time
import json
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup


def get_links(link: str, pod_name: str):
    # Setup the WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)  # Increased implicit wait for better handling of load times
    driver.get(link)

    output_filename = f"transcript_links/transcript_links_{pod_name}.txt"
    j = 0  # Initialize index for new links
    with open(output_filename, 'w') as file:
        while True:
            try:
                # Refined XPath for "See More" button
                loadmore_elements = driver.find_elements(By.XPATH, "//button[text()='See More']")
                
                if loadmore_elements and loadmore_elements[0].is_displayed():
                    button = loadmore_elements[0]

                    # Scroll to the button's position
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                    time.sleep(1)  # Slightly increased wait to ensure the button is scrolled into view

                    # Wait until the button is clickable and click it
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button)).click()
                    time.sleep(5)  # Allow time for new elements to load
                else:
                    print("No more 'See More' button to click.")
                    break
            except ElementClickInterceptedException:
                print("Element click intercepted. Trying again...")
                time.sleep(2)  # Wait a moment before retrying
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
    return output_filename



def get_transcription(url : str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape transcription text
        transcriptions = soup.find_all('span', class_='podcast-transcription-text')
        transcription_text = ' '.join([text.get_text() for text in transcriptions])
        # Scrape episode title
        title_element = soup.find('span', {'data-test': 'truncate-span'})

        if title_element:
            episode_title = title_element.get_text(strip = True)
        else:
            episode_title = "Title not found"

        date_len_element = soup.find('div', class_ = 'css-1479fkt egx951j0')

        if date_len_element:
            date_length = date_len_element.get_text(strip = True)
            split_info = date_length.split("•")
            episode_date = split_info[0]
            episode_length = (split_info[1]).split(" ")[0]
        
        return episode_title, episode_date, episode_length, transcription_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None, None


def process_links_from_file(filename : str, pod_name: str):
    podcasts = {}  # Dictionary to hold podcasts and their episodes
    with open(filename, 'r') as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip() 
        print(f"Processing {url}...")

        episode_title, episode_date, episode_length, transcription = get_transcription(url)

        if episode_title and transcription:
            print(f"Collected transcription for {url}: {episode_title}")

            # Create a dictionary for the episode
            episode_data = {
                "episode_title": episode_title,
                "episode date": episode_date,
                "episode_length": episode_length,
                "transcription": transcription
            }

            # If podcast is already in the dictionary, append the episode
            if pod_name in podcasts:
                podcasts[pod_name].append(episode_data)
            else:
                podcasts[pod_name] = [episode_data]

        else:
            print(f"Failed to fetch transcription for {url}.")

    # Save all podcasts to a JSON file
    with open(f"json_files/podcast_data{pod_name}.json", 'w') as json_file:
        json.dump(podcasts, json_file, indent=4)

    print("Finished processing all links.")


def complete_task(start_url :str, pod_name: str):
    # Get transcription links and podcast/episode information 
    links_file = get_links(start_url, pod_name)

    # Step 2: Process the transcription links and save podcast/episode info to a json file
    process_links_from_file(links_file, pod_name)


# The line below shows an example of the function you can run and an input to test the above functionality 


#complete_task('https://www.iheart.com/podcast/1119-the-bobby-bones-show-25100459/', pod_name = 'Bobby Bones Test' )
process_links_from_file('transcript_links/transcript_links_bobby_bones.txt', pod_name = 'Test' )

