from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from datetime import datetime

driver_path = "C:\\chromedriver\\chromedriver.exe"

chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

options = Options()
options.binary_location = chrome_path

service = Service(driver_path)


def parse_tournament_info(input_string: str) -> dict:
    pattern = r"ATP - SINGLES: ([A-Za-z\s]+) \(([^)]+)\), ([A-Za-z\s]+)(?: \((indoor)\))? - ([A-Za-z\s0-9/-]+)"
    match = re.match(pattern, input_string, re.IGNORECASE)
    if match:
        return {
            'tournament_name': match.group(1).strip(),
            'location': match.group(2).strip(),
            'surface': match.group(3).strip(),
            'court': match.group(4).strip() if match.group(4) else 'outdoor',
            'round_name': match.group(5).strip()
        }
    return {}


def parse_time_and_date(input_string: str) -> dict:
    parts = input_string.split(" ")
    input_string = ' '.join(parts)

    parsed_datetime = datetime.strptime(input_string, '%I:%M %p, %B %d, %Y')
    time = parsed_datetime.strftime('%H:%M')
    date = parsed_datetime.strftime('%Y-%m-%d')

    return {'date': date, 'time': time}


def parse_player_rank(input_string: str) -> str:
    match = re.search(r'\d+', input_string)
    return match.group() if match else ""


def parse_player_seed_or_entry(input_string: str) -> str:
    text_without_brackets = input_string.replace("(", "").replace(")", "")
    return text_without_brackets


# Data Extraction Functions
def extract_player_details(player_element) -> dict:
    name = player_element.find_element(By.CLASS_NAME, "participant__participantName.participant__overflow").text
    try:
        rank = parse_player_rank(
            player_element.find_element(By.CLASS_NAME, "participant__participantRank").text
        )
    except Exception:
        rank = ""
    winner = 'duelParticipant--winner' in player_element.get_attribute("class")
    return {'name': name, 'rank': rank, 'is_winner': winner}


def change_url_to_bracket(url: str) -> str:
    new_url = url.replace("/game-summary", "/draw")
    return new_url


def get_player_seed(participant_rows, target_name):
    for row in participant_rows:
        try:
            name_element = row.find_element(By.CLASS_NAME, "bracket__name")
            if name_element.text.strip() == target_name:
                info_element = row.find_element(By.CLASS_NAME, "bracket__info")
                number = info_element.text.strip()
                return parse_player_seed_or_entry(number)
        except Exception as e:
            continue


def parse_odds_text(text):
    result = re.findall(r'\d+\.\d+', text)

    if result:
        extracted_number = result[0]
    else:
        extracted_number = "1.8"
    return extracted_number


def get_odds(odds_div):
    cell_wrappers = odds_div.find_elements(By.CLASS_NAME, "cellWrapper")

    odds_1 = cell_wrappers[0].get_attribute("title").split("»")[-1].strip()
    odds_2 = cell_wrappers[1].get_attribute("title").split("»")[-1].strip()
    return parse_odds_text(odds_1), parse_odds_text(odds_2)


# Main Scraper Logic
def scrape_match_summary(driver, match_link) -> dict:
    data = {}

    tournament_info = driver.find_element(By.CSS_SELECTOR, "span.tournamentHeader__country")
    data['tournament_info'] = parse_tournament_info(tournament_info.text)

    time_and_date = driver.find_element(By.CLASS_NAME, "duelParticipant__startTime")
    data['time_and_date'] = parse_time_and_date(time_and_date.text)
    player1 = driver.find_element(By.CLASS_NAME, "duelParticipant__home")
    player2 = driver.find_element(By.CLASS_NAME, "duelParticipant__away")
    data['player1'] = extract_player_details(player1)
    data['player2'] = extract_player_details(player2)

    odds_div = driver.find_element(By.CLASS_NAME, "oddsNotClickable")
    player1_odds, player2_odds = get_odds(odds_div)
    data['player1']['odds'] = player1_odds
    data['player2']['odds'] = player2_odds

    driver.get(change_url_to_bracket(match_link))
    participant_rows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "bracket__participantRow"))
    )
    data['player1']['seed'] = get_player_seed(participant_rows, data['player1']['name'])
    data['player2']['seed'] = get_player_seed(participant_rows, data['player2']['name'])

    return data


def change_url_to_statistics(url: str) -> str:
    new_url = url + "/game-statistics"
    return new_url


def get_scheduled_match_details(match_links):
    driver = webdriver.Chrome(service=service, options=options)
    output = {}
    try:
        for match_link in match_links:
            driver.get(match_link)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.tournamentHeader__country"))
            )

            match_summary = scrape_match_summary(driver, match_link)

            match_data = {
                "match_summary": match_summary,
            }
            output[match_link] = match_data


    except Exception as e:
        print(f"Error occurred: {e}")
        raise e

    finally:
        driver.quit()
    return output
