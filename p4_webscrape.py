"""
Carter Moser
Cam Christopher
Zackery Schaub
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plot

standard_works_dict = {
            'Speaker_Name': '', 'Talk_Name': '', 'Kicker': '',
            'Matthew': 0, 'Mark': 0, 'Luke': 0, 'John': 0, 'Acts': 0,
            'Romans': 0, '1 Corinthians': 0, '2 Corinthians': 0, 'Galatians': 0,
            'Ephesians': 0, 'Philippians': 0, 'Colossians': 0, '1 Thessalonians': 0,
            '2 Thessalonians': 0, '1 Timothy': 0, '2 Timothy': 0, 'Titus': 0,
            'Philemon': 0, 'Hebrews': 0, 'James': 0, '1 Peter': 0, '2 Peter': 0,
            '1 John': 0, '2 John': 0, '3 John': 0, 'Jude': 0, 'Revelation': 0,
            'Genesis': 0, 'Exodus': 0, 'Leviticus': 0, 'Numbers': 0,
            'Deuteronomy': 0, 'Joshua': 0, 'Judges': 0, 'Ruth': 0, '1 Samuel': 0,
            '2 Samuel': 0, '1 Kings': 0, '2 Kings': 0, '1 Chronicles': 0,
            '2 Chronicles': 0, 'Ezra': 0, 'Nehemiah': 0, 'Esther': 0, 'Job': 0,
            'Psalm': 0, 'Proverbs': 0, 'Ecclesiastes': 0, 'Song of Solomon': 0,
            'Isaiah': 0, 'Jeremiah': 0, 'Lamentations': 0, 'Ezekiel': 0,
            'Daniel': 0, 'Hosea': 0, 'Joel': 0, 'Amos': 0, 'Obadiah': 0,
            'Jonah': 0, 'Micah': 0, 'Nahum': 0, 'Habakkuk': 0, 'Zephaniah': 0,
            'Haggai': 0, 'Zechariah': 0, 'Malachi': 0, '1 Nephi': 0, '2 Nephi': 0,
            'Jacob': 0, 'Enos': 0, 'Jarom': 0, 'Omni': 0, 'Words of Mormon': 0,
            'Mosiah': 0, 'Alma': 0, 'Helaman': 0, '3 Nephi': 0, '4 Nephi': 0,
            'Mormon': 0, 'Ether': 0, 'Moroni': 0, 'Doctrine and Covenants': 0,
            'Moses': 0, 'Abraham': 0, 'Joseph Smith---Matthew': 0,
            'Joseph Smith---History': 0, 'Articles of Faith': 0
            }

engine = sqlalchemy.create_engine('postgresql://postgres:Mahay2004@localhost/is303')

user_input = input("If you want to scrape data, enter 1. If you want to see summaries of stored data, enter 2. Enter any other value to exit the program: ")


if user_input == '1':
    # Part 1 code
    drop_table_query = sqlalchemy.text("drop table if exists general_conference;")
    conn = engine.connect()
    conn.execute(drop_table_query)
    conn.commit
    conn.close()
    #Scrape
    base_url = 'https://www.churchofjesuschrist.org'
    main_url = 'https://www.churchofjesuschrist.org/study/general-conference/2026/04?lang=eng'

    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links on the page
    all_links = soup.find_all('a', href=True)

    talk_urls = []
    
    for link in all_links :
        href = link['href']
    # Only keep links that are individual talks
        if '/study/general-conference/2025/10/' in href:
            # Skip session and sustaining pages
            if 'session' in href.lower() or 'sustaining' in href.lower():
                continue
            full_url = base_url + href
            if full_url not in talk_urls:  # avoid duplicates
                talk_urls.append(full_url)
    
    #Need to pull data from each individual talk.
    for url in talk_urls :
     
elif user_input == '2':
    # Part 2 code
     
else:
    print("Closing the program.")
