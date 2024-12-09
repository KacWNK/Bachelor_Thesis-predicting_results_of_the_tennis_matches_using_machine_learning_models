import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timedelta
import json

results = {}
unwanted_tournaments = ["challenger", "futures", "itf", "utr", "seniors", "a day at the drive", "bundesliga", "czech league", "german championships", "laver cup", "exh", "World Tennis League", "Masters Cup ATP", "Next Gen ATP Finals", 'Melbourne Summer Set']
# Define the start and end dates for iteration
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 12, 31)
current_date = start_date
while current_date <= end_date:
    year = current_date.year
    month = current_date.month
    day = current_date.day

    # Construct the URL with the current date
    main_url = f"https://www.tennisexplorer.com/results/?type=atp-single&year={year}&month={month:02d}&day={day:02d}"
    print(f"Processing URL: {main_url}")
    response = requests.get(main_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    right_div = soup.find("div", id="right")
    if right_div:
        right_div.decompose()
    table = soup.find("table", class_="result")

    for row in table.find_all("tr"):
        tname_element = row.find("td", class_="t-name")

        if not tname_element:
            continue
        type_men2_span = tname_element.find("span", class_="type-men2")
        if type_men2_span:
            tournament_name = tname_element.get_text(strip=True)
            # Condition to stop scraping (e.g., if the tournament name contains "Challenger")
            if any(tournament_type.lower() in tournament_name.lower() for tournament_type in unwanted_tournaments):
                print(f"Stopping scraping: Unwanted tournament found ({tournament_name}).")
                break
            if tournament_name not in results:
                results[tournament_name] = {}
            print(f"Processing tournament: {tournament_name}")

        links = row.find_all("a", href=True)
        if not links:
            continue

        for link in links:
            if 'match-detail' in link["href"]:
                match_url = urljoin(main_url, link["href"])
                print(f"Visiting match detail page: {match_url}")

                match_response = requests.get(match_url)
                match_response.raise_for_status()

                # Parse the match detail page
                match_soup = BeautifulSoup(match_response.content, "html.parser")
                center_div = match_soup.find("div", id="center")
                player_elements = center_div.find_all("th", class_="plName")
                player_names = [element.find("a").get_text(strip=True) for element in player_elements]

                print("Player Names:", player_names)
                match_info_div = center_div.find("div", class_="box boxBasic lGray")

                if match_info_div:
                    date = match_info_div.find("span", class_="upper").get_text(strip=True)

                    text_parts = match_info_div.get_text(separator=" ", strip=True).split(", ")
                    time = text_parts[1].strip()
                    round_info = text_parts[3].strip()


                    print(f"Date: {date}")
                    print(f"Time: {time}")
                    print(f"Round: {round_info}")
                    match_data = {
                        "Player1": player_names[0],
                        "Player2": player_names[1],
                        "Time": time,
                        "Date": date,
                    }
                    print('****')
                    print(tournament_name)
                    if round_info not in results[tournament_name]:
                        results[tournament_name][round_info] = []

                    results[tournament_name][round_info].append(match_data)
    current_date += timedelta(days=1)
print(results)
output_file = "scraped_match_time_2021.json"

with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)

print(f"Results have been saved to {output_file}")