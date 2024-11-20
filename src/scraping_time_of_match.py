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
    # Send a GET request to the page
    response = requests.get(main_url)
    response.raise_for_status()  # Ensure the request was successful

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    right_div = soup.find("div", id="right")
    if right_div:
        right_div.decompose()
    # Find the table with the specific class (e.g., "target-table")
    table = soup.find("table", class_="result")

    for row in table.find_all("tr"):
        # Find the <td> element with class 't-name' in the row
        tname_element = row.find("td", class_="t-name")

        # If no 't-name' element is found, skip this row
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

        # Extract the <a> tag within the 't-name' element
        links = row.find_all("a", href=True)
        if not links:
            continue

        for link in links:
            if 'match-detail' in link["href"]:
                match_url = urljoin(main_url, link["href"])
                print(f"Visiting match detail page: {match_url}")

                # Send a request to the match detail page
                match_response = requests.get(match_url)
                match_response.raise_for_status()

                # Parse the match detail page
                match_soup = BeautifulSoup(match_response.content, "html.parser")
                center_div = match_soup.find("div", id="center")
                player_elements = center_div.find_all("th", class_="plName")
                player_names = [element.find("a").get_text(strip=True) for element in player_elements]

                # Print the extracted player names
                print("Player Names:", player_names)
                match_info_div = center_div.find("div", class_="box boxBasic lGray")

                # Check if the div was found
                if match_info_div:
                    # Extract the date (from <span> with class 'upper')
                    date = match_info_div.find("span", class_="upper").get_text(strip=True)

                    # Extract the remaining text content (after the date)
                    text_parts = match_info_div.get_text(separator=" ", strip=True).split(", ")
                    # Extract time, tournament name, and round
                    time = text_parts[1].strip()
                    #tournament_name = match_info_div.find("a").get_text(strip=True)
                    round_info = text_parts[3].strip()

                    # Print the extracted information
                    #print(f"Tournament: {tournament_name}")
                    print(f"Date: {date}")
                    print(f"Time: {time}")
                    print(f"Round: {round_info}")
                    # Store match details in results
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

# Save the results dictionary to a JSON file
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)

print(f"Results have been saved to {output_file}")