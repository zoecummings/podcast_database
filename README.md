# Podcast Data Scraper and Database
This repository contains two major sections
1. A tool used to scrape podcast data **specifically from [iHeartRadio](https://www.iheart.com/podcast/category/top-overall-132/)**
2. A database to store the scraped podcast data
## Project Motivation

In the SNaPP Lab at William and Mary I am a part of a team looking into podcast data over time. After having solidified our research design and the scope of the project this semester, we have moved towards data collection. Our original data collection method involved manual recording of the audio and transcribing the collected mp3 files. Around half way through this semester we found that iHeartRadio had begun posting transcriptions for individual podcast episodes which opened the door for a new and more efficient data collection method. As I started working on creating the script to scrape the podcast information and transcriptions I realized I was often relying on the automation techniques and organization principles we had been learning this semester which is why I ultimately decided to continue my work on this data collection and storage for the DATA 440 final project. As well as improving the efficiency of my data collection code I also wanted to have detailed instructions for future lab members on how this can be replicated moving forward. For the non data science members I decided to have a database with the information and the option to download the data as a CSV file for overall usage for a range of data science skills. This gave an opportunity to spend more time learning about web scraping particulary for pages with more roadblocks such as a "see more" button. 

You can see more about the motivation as well as the scope of the work for this class in the project proposal! 

## Transcription Web Scraper

### First Steps

Before using this code you will need to ensure you have met certain requirements.
You will need to install these if you have not already, and then within the get_transcripts.py file them will be imported. 
Install the required dependencies using pip.

Selenium
BeautifulSoup
requests
ChromeDriver


Example Installation:

```python
pip install selenium beautifulsoup4 requests
```

You will also need to download ChromeDriver:
- Download the appropriate version of ChromeDriver based on your Chrome version and ensure that it is in your system's PATH.

### Functions

The **iHeartRadio** podcast web scraping tool consists of multiple Python functions. The functions their useage and purpose include: 

1. ```get_links()```
   
     This function extracts all the links to podcast transcriptions by navigating through the podcast page and clicking the "See More" button to reveal additional episodes.
     This function takes the longest time to run as you need to wait for the pages to load as the computer presses the button and loads more data. 

     **Parameters:**
   
     - link: The URL of the iHeartRadio podcast page (string).
     - pod_name: The name of the podcast (string, used for file names).
     
     
     This will scrape all episode links and save them to a file named transcript_links_{pod_name}.txt in the json_files folder

2. ```get_transcription()```
   
     This function extracts transcriptions, episode titles, dates, and lengths (in minutes) from a specific podcast episode URL.
     
     **Parameters:**
   
     - url: The URL of the podcast episode (this must be a specific episode from iHeartRadio that has the transcript available)

     This will return the episode's title, date, length, and the transcription text.

     It can be called on its on with the url being the link to an iHeartRadio page that has the transcription and information on a single episode of a podcast, or it         can be called within the ```process_links_from_file()``` function. 

3. ```process_links_from_file()```
   
     This function processes the links saved in a text file (transcript_links_{pod_name}.txt) saved in the json_files folder.

     This takes the episode name, date, length and transcription from the get_transcriptions() function and saves them in a nested dictionary structure through a json file.

   
    **Parameters:**
     - filename: The file containing the episode links (transcript_links_{pod_name}.txt).
     - pod_name: The name of the podcast, which will be used to name the output JSON file.

     Example of json structure:
   
  ```json
     {
    "Bobby Bones Show": [
        {
            "episode_title": "Tues Post Show: Lunchbox Makes An Empty Promise, DIY Dental Work And Trapped In An Elevator \u00a0(12-17-24)",
            "episode date": "December 17, 2024",
            "episode_length": "55",
            "transcription": "It's time for the Bobby Bones post show.
        }
```

4. ```complete_task()```

This function automates the entire process: it extracts the episode links, scrapes the transcription data, and saves the results into a JSON file. It does this by calling the get_links() and process_links_from_file() functions. 

**This is the function I recommend using if you want to see the entire data collection process through. Note that you want to give yourself at least an hour to collect data as by the nature of web scraping with a "see more" button it is easiest to do it all at once which is what this code supports.**

Parameters:
- start_url: The URL of the overall podcast page
- pod_name: The name of the podcast.






