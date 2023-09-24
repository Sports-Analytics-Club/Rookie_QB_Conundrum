import string
import requests
from bs4 import BeautifulSoup

alphabet = list(string.ascii_uppercase)

base_url = "https://www.pro-football-reference.com/"

# Create a QB_Data file that contains the parsed html files.
import os 
os.mkdir("QB_Data")

for letter in alphabet:
    url = f"{base_url}/players/{letter}/"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    player_elements = soup.find_all('div', class_='players')

    for player in player_elements:
       player_link = player.find('a', href=True)
       player_url = f"{base_url}{player_link['href']}"

       player_response = requests.get(player_url)
       player_soup = BeautifulSoup(player_response.text, 'html.parser')

       player_info = player_soup.find('div', {'itemtype': 'https://schema.org/Person'}).text

       # Extracting position and start year
       position_start_year = player_info.split(')')[1].strip()

       if "QB" in position_start_year and int(position_start_year.split('-')[0]) >= 1966:
           with open(f"QB_Data/{player_link['href'].split('/')[1]}.html", "w+") as file:
               file.write(player_response.text)