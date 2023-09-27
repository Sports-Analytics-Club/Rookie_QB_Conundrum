import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Define url template and letters
url_template = "https://www.pro-football-reference.com/players/{}/"
letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

# Function to scrape player links for a given letter
def get_quarterbacks(letter):
    url = url_template.format(letter)
    response = requests.get(url)
    time.sleep(8)

    soup = BeautifulSoup(response.text, 'html.parser')

    players = []
    for p in soup.select('#div_players p'):
        meta = p.get_text()
        position = str(meta.split('(')[1].split(')')[0])
        is_qb = 1 if 'QB' in position else 0
        year_span = meta.split(')')[1].strip()
        start_year = int(year_span.split('-')[0])
        end_year = int(year_span.split('-')[1])
        slug = p.find('a')['href']
        full_slug = f"https://www.pro-football-reference.com{slug}"
        if is_qb == 1:
            players.append([meta, position, year_span, start_year, end_year, full_slug])
    df = pd.DataFrame(players, columns=['meta', 'position', 'year_span', 'start_year', 'end_year', 'full_slug'])
    df['iter'] = letter # Add the letter for debugging
    return df


# Scrape all player links for all letters
all_players = pd.concat([get_quarterbacks(letter) for letter in letters], ignore_index=True)

# Save data to csv file
all_players.to_csv("player_links.csv", index="False")