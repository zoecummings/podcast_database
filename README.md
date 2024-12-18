# Podcast Data Scraper and Database
This repository contains to major sections
1. A tool used to scrape podcast data **specifically from [iHeartRadio](https://www.iheart.com/podcast/category/top-overall-132/)**
2. A database to store the scraped podcast data
     - priliminary visualizations using this data
## Transcription Web Scraper

The **iHeartRadio** podcast web scraping tool consists of multiple Python functions. The functions their useage and purpose include: 

1. ```get_links()```
   
This function extracts all the links to podcast transcriptions by navigating through the podcast page and clicking the "See More" button to reveal additional episodes.

Parameters:
link: The URL of the iHeartRadio podcast page (e.g., https://www.iheart.com/podcast/1119-stuff-you-should-know-26940277/).
pod_name: The name of the podcast (used to save the output file with a meaningful name).
Example:
python
Copy code
get_links('https://www.iheart.com/podcast/1119-stuff-you-should-know-26940277/', pod_name='HowStuffWorks')
This will scrape all episode links and save them to a file named transcript_links_HowStuffWorks.txt.

2. ```get_transcription()```
This function extracts transcriptions, episode titles, dates, and lengths from a specific podcast episode URL.

Parameters:
url: The URL of the podcast episode (e.g., https://www.iheart.com/podcast/1119-stuff-you-should-know-26940277/episode/episode-name/#transcription).
Example:
python
Copy code
get_transcription('https://www.iheart.com/podcast/1119-stuff-you-should-know-26940277/episode/episode-name/#transcription')
This will return the episode's title, date, length, and the transcription text.

3. ```process_links_from_file()```
This function processes the links saved in a text file, scrapes transcription data for each link, and saves all podcast episode data into a JSON file.

Parameters:
filename: The file containing the episode links (output from get_links).
pod_name: The name of the podcast, which will be used to name the output JSON file.
Example:
python
Copy code
process_links_from_file('transcript_links_HowStuffWorks.txt', 'HowStuffWorks')
This will scrape transcriptions for each episode link and save the data in a JSON file named podcast_dataHowStuffWorks.json.

4. ```complete_task()```
This function automates the entire process: it extracts the episode links, scrapes the transcription data, and saves the results into a JSON file.

Parameters:
start_url: The URL of the podcast page (e.g., https://www.iheart.com/podcast/1119-stuff-you-should-know-26940277/).
pod_name: The name of the podcast.
Example:
python
Copy code
complete_task('https://www.iheart.com/podcast/1119-stuff-you-should-know-26940277/', pod_name='HowStuffWorks')
This will run the entire process, saving the transcription links and episode data in podcast_dataHowStuffWorks.json.
