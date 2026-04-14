f"""
Carter Moser
Cam Christopher
Zackery Schaub
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plot
import copy

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
    conn.commit()
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
        if '/study/general-conference/2026/04/' in href:
            # Skip session and sustaining pages
            if 'session' in href.lower() or 'sustaining' in href.lower():
                continue
            full_url = base_url + href
            if full_url not in talk_urls:  # avoid duplicates
                talk_urls.append(full_url)
    
    #Need to pull data from each individual talk.
    all_talks = []

    for url in talk_urls :
        current_talk = copy.deepcopy(standard_works_dict)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract basic info
        title_tag = soup.find('h1')
        speaker_tag = soup.find('p', class_='author-name')
        kicker_tag = soup.find('p', class_='kicker')

        current_talk['Talk_Name'] = title_tag.get_text(strip=True) if title_tag else ''
        current_talk['Speaker_Name'] = speaker_tag.get_text(strip=True).replace("By ", "") if speaker_tag else ''
        current_talk['Kicker'] = kicker_tag.get_text(strip=True) if kicker_tag else ''

        # Count scripture references
        references = soup.find_all('a', class_='scripture-ref') or []

        books = sorted(
            [b for b in current_talk if b not in ['Speaker_Name', 'Talk_Name', 'Kicker']],
            key=len,
            reverse=True
        )

        for ref in references:
            text = ref.get_text()

            for book in books:
                if book in text:
                    current_talk[book] += 1
                    break

        all_talks.append(current_talk)

    df = pd.DataFrame(all_talks)
    df.to_sql('general_conference', engine, index=False, if_exists='replace')
    print("You've saved the scraped data to your postgres database.")
     



elif user_input == '2':
    print("You selected to see summaries. Enter 1 to see a summary of all talks. Enter 2 to select a specific talk. Enter anything else to exit: ")
    choice = input()

    # Load data from Postgres
    df = pd.read_sql('general_conference', engine)

    if choice == '1':
        # Get all book columns
        book_columns = [col for col in df.columns if col not in ['Speaker_Name', 'Talk_Name', 'Kicker']]

        # Sum all references across talks
        totals = df[book_columns].sum()

        # Only keep books with more than 2 references
        filtered = totals[totals > 2]

        # Plot
        plot.figure()
        filtered.plot(kind='bar')

        plot.title('Standard Works Referenced in General Conference')
        plot.xlabel('Standard Works Books')
        plot.ylabel('# Times Referenced')

        plot.xticks(rotation=90)
        plot.tight_layout()
        plot.show()

    elif choice == '2':
        print("The following are the names of speakers and their talks:")

        # Display numbered list
        for i, row in df.iterrows():
            print(f"{i+1}: {row['Speaker_Name']} – {row['Talk_Name']}")

        # Get user selection
        selection = int(input("Please enter the number of the talk you want to see summarized: "))

        # Validate selection
        if selection < 1 or selection > len(df):
            print("Invalid selection.")
        else:
            selected_row = df.iloc[selection - 1]

            # Get book columns
            book_columns = [col for col in df.columns if col not in ['Speaker_Name', 'Talk_Name', 'Kicker']]

            # Get data for that talk
            talk_data = selected_row[book_columns]

            # Only keep books with at least 1 reference
            filtered = talk_data[talk_data > 0]

            # Plot
            plot.figure()
            filtered.plot(kind='bar')

            plot.title(f"Standard Works Referenced in: {selected_row['Talk_Name']}")
            plot.xlabel('Standard Works Books')
            plot.ylabel('# Times Referenced')

            plot.xticks(rotation=90)
            plot.tight_layout()
            plot.show()

    else:
        print("Closing the program.")
