import requests
from bs4 import BeautifulSoup
import json

player_links = []

response = requests.get("https://www.tennisexplorer.com/list-players/")
response.raise_for_status()
soup = BeautifulSoup(response.content, 'html.parser')
center_div = soup.find('div', id='center')

rows = center_div.find_all('tr', class_=['one', 'two'])

country_links = [a['href'] for row in rows for a in row.find_all('a', href=True)]
for link in country_links:
    print(link)
    page_number = 1
    while True:
        print(page_number)
        response = requests.get(f'https://www.tennisexplorer.com/list-players/{link[2:]}&page={page_number}')
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        center_div = soup.find('div', id='center')

        divs = center_div.find_all('table', class_='result')
        target_divs = []
        for div in divs:
            if not div.find_parent('form', id='playerSearch'):
                target_divs.append(div)
        if not target_divs:
            break

        rows = target_divs[0].find_all('tr', class_=['one', 'two'])
        stop_iteration = False
        for row in rows:
            rank = row.find('td', class_='first rank').get_text()
            if rank.isspace():
                stop_iteration = True
                break
            td_name = row.find('td', class_='t-name')
            player_link = td_name.find('a', href=True)['href']
            player_links.append(f'https://www.tennisexplorer.com{player_link}')

        if stop_iteration:
            break

        page_number += 1

with open("../../data/tennis_explorer_scraped/player_info_links.json", "w") as file:
    json.dump(player_links, file, indent=4)
