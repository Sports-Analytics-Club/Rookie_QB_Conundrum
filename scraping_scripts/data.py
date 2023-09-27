import string
import requests
from bs4 import BeautifulSoup

alphabet = list(string.ascii_uppercase)

base_url = "https://www.pro-football-reference.com/players/"

for letter in alphabet:
    url = f"{base_url}{letter}/"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    section_wrapper = soup.find('div', class_='section_wrapper', id='all_players')
    section_content = section_wrapper.find('div', class_='section_content', id='div_players')
    p_tags = section_content.find_all('p')

    for p in p_tags:
        # Extract player name and years
        player_name = p.find('a').text
        player_years = p.find_next('a').text

        if "(QB)" in player_name and "2020" in player_years:
            player_link = p.find('a')['href']
            print(f"Player Name: {player_name}")
            print(f"Player Link: {player_link}")
            with open("//QB_Data/{player_link}", "w+") as f:
                f.write(player_link)