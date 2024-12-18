import os
import sqlite3
import numpy as np
import pandas as pd
import json

#function to create four tables which store podcast data
def create_database(db_name='podcast_data.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS podcast_metadata (
                        podcast_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        podcast_name TEXT,
                        pod_description TEXT,
                        transcript_exist BOOLEAN,
                        ideology TEXT,
                        ideology_id INTEGER
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS episode_metadata (
                        episode_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        podcast_id INTEGER,
                        episode_name TEXT,
                        date TEXT,
                        ep_description TEXT,
                        length TEXT,
                        FOREIGN KEY (podcast_id) REFERENCES podcast_metadata (podcast_id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS popularity (
                        podcast_id INTEGER,
                        rank INTEGER,
                        date TEXT,
                        FOREIGN KEY (podcast_id) REFERENCES podcast_metadata (podcast_id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transcripts (
                        podcast_id INTEGER,
                        episode_id INTEGER,
                        transcript TEXT,
                        FOREIGN KEY (podcast_id) REFERENCES podcast_metadata (podcast_id),
                        FOREIGN KEY (episode_id) REFERENCES episode_metadata (episode_id)
                    )''')

    conn.commit()
    conn.close()

create_database()



def insert_podcast_metadata(podcast_name, transcript_exist, ideology, ideology_id):
    conn = sqlite3.connect('podcast_data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO podcast_metadata (podcast_name, transcript_exist, ideology, ideology_id) 
                      VALUES (?, ?, ?, ?)''', 
                   (podcast_name, transcript_exist, ideology, ideology_id))
    conn.commit()
    podcast_id = cursor.lastrowid
    conn.close()
    return podcast_id

def insert_episode_metadata(podcast_id, episode_name, date, length):
    conn = sqlite3.connect('podcast_data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO episode_metadata (podcast_id, episode_name, date, length) 
                      VALUES (?, ?, ?, ?)''', 
                   (podcast_id, episode_name, date, length))
    conn.commit()
    episode_id = cursor.lastrowid
    conn.close()
    return episode_id

def insert_popularity(podcast_id, rank, date):
    conn = sqlite3.connect('podcast_data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO popularity (podcast_id, rank, date) 
                      VALUES (?, ?, ?)''', 
                   (podcast_id, rank, date))
    conn.commit()
    conn.close()

def insert_transcript(podcast_id, episode_id, transcript):
    conn = sqlite3.connect('podcast_data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO transcripts (podcast_id, episode_id, transcript) 
                      VALUES (?, ?, ?)''', 
                   (podcast_id, episode_id, transcript))
    conn.commit()
    conn.close()

def process_json_data(filename, pod_name):
    # Load the JSON data from the file
    with open(filename, 'r') as file:
        podcasts_data = json.load(file)

    # Insert podcast metadata and then episode metadata into the database
    if pod_name in podcasts_data:
        podcast_info = podcasts_data[pod_name]

        # Insert podcast metadata into the database
        # This is currently hard coded but in future applications I would like to swith this as we gain ideology data and bring in data that does not have transcripts yet. 
        podcast_id = insert_podcast_metadata(pod_name, True, 'NA', 'NA')

        # Iterate through episodes and insert data
        for episode in podcast_info:
            episode_title = episode.get('episode_title')
            episode_date = episode.get('episode_date')
            episode_length = episode.get('episode_length')
            transcription = episode.get('transcription')

            # Insert episode metadata into the database
            episode_id = insert_episode_metadata(podcast_id, episode_title, episode_date, episode_length)

            # Insert transcript into the database
            insert_transcript(podcast_id, episode_id, transcription)

        print(f"Finished processing data for {pod_name}.")


process_json_data('json_files/podcast_dataBobby Bones Show.json', 'Bobby Bones Show')