import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json

with open("../../data/tennis_explorer_scraped/player_info_links.json", "r") as file:
    player_links = json.load(file)


all_player_details = []

for player_link in player_links:
    response = requests.get(player_link)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    player_detail_table = soup.find('table', class_='plDetail')

    if not player_detail_table:
        continue

    name = player_detail_table.find('h3').get_text()

    details = player_detail_table.find_all('div', class_='date')

    player_details = {"Name": name}
    for detail in details:
        text = detail.get_text()
        if text.startswith("Country:"):
            player_details['Country'] = text.split("Country: ")[1]
        elif text.startswith("Height / Weight:"):
            player_details['Height'] = text.split("Height / Weight: ")[1].split(' / ')[0]
        elif text.startswith("Age:"):
            match = re.search(r'\((\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})\)', text)
            if match:
                day, month, year = map(int, match.groups())

                birth_date = datetime(year, month, day).strftime('%Y-%m-%d')
                print(f"Formatted Date: {birth_date}")
                player_details['Date_of_birth'] = birth_date
            else:
                print("Date not found")
        elif text.startswith("Plays:"):
            player_details['Plays'] = text.split("Plays: ")[1]

    print(player_details)
    all_player_details.append(player_details)

all_player_details_json = json.dumps(all_player_details, indent=4)

with open("../../data/raw_data/player_details.json", "w") as json_file:
    json_file.write(all_player_details_json)

print("Player details saved to 'player_details.json'")
