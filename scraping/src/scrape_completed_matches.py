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


def parse_score(input_string: str, player1_won: bool) -> dict:
    input_string = input_string.replace("\n", "")
    if player1_won:
        return {"Wsets": int(input_string[0]), "Lsets": int(input_string[2])}
    return {"Wsets": int(input_string[2]), "Lsets": int(input_string[0])}


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


def extract_seed_details(smh_div, driver, side: str) -> str:
    parent_div = smh_div.find_element(By.CLASS_NAME, f"smh__participantName.smh__{side}")
    driver.implicitly_wait(0)
    try:
        seed_or_entry_element = parent_div.find_element(By.CSS_SELECTOR, "span.smh__startPosition")
        return parse_player_seed_or_entry(seed_or_entry_element.text)
    except:
        return ""
    finally:
        driver.implicitly_wait(10)


def get_player_score_parts(smh_div, sets_played: int) -> dict:
    scores = {'player1': {}, 'player2': {}}
    for i in range(1, sets_played + 1):
        scores['player1'][f"Set {i}"] = smh_div.find_element(By.CLASS_NAME, f"smh__part.smh__home.smh__part--{i}").text
        scores['player2'][f"Set {i}"] = smh_div.find_element(By.CLASS_NAME, f"smh__part.smh__away.smh__part--{i}").text
    return scores


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
def scrape_match_summary(driver) -> dict:
    data = {}

    tournament_info = driver.find_element(By.CSS_SELECTOR, "span.tournamentHeader__country")
    data['tournament_info'] = parse_tournament_info(tournament_info.text)

    time_and_date = driver.find_element(By.CLASS_NAME, "duelParticipant__startTime")
    data['time_and_date'] = parse_time_and_date(time_and_date.text)
    comment = driver.find_element(By.CLASS_NAME, "detailScore__status").text
    player1 = driver.find_element(By.CLASS_NAME, "duelParticipant__home")
    player2 = driver.find_element(By.CLASS_NAME, "duelParticipant__away")
    data['player1'] = extract_player_details(player1)
    data['player2'] = extract_player_details(player2)

    odds_div = driver.find_element(By.CLASS_NAME, "oddsNotClickable")
    player1_odds, player2_odds = get_odds(odds_div)
    data['player1']['odds'] = player1_odds
    data['player2']['odds'] = player2_odds

    data['comment'] = comment
    if comment.strip() and comment != "WALKOVER" and comment != "CANCELLED":
        smh_div = driver.find_element(By.CLASS_NAME, "smh__template.tennis")
        data['player1']['seed'] = extract_seed_details(smh_div, driver, "home")
        data['player2']['seed'] = extract_seed_details(smh_div, driver, "away")

        sets_score = parse_score(driver.find_element(By.CLASS_NAME, "detailScore__wrapper").text,
                                 data['player1']['is_winner'])
        data['sets_score'] = sets_score

        sets_played = sets_score["Wsets"] + sets_score["Lsets"]
        data['scores_by_set'] = get_player_score_parts(smh_div, sets_played)

        sets_played = sets_score["Wsets"] + sets_score["Lsets"]
        data['scores_by_set'] = get_player_score_parts(smh_div, sets_played)

        try:
            duration = smh_div.find_element(By.CLASS_NAME, "smh__time.smh__time--overall").text
            data['duration'] = duration
        except Exception:
            data['duration'] = "N/A"

    return data


def scrape_match_statistics(driver) -> dict:
    statistics = {}
    categories_divs = driver.find_elements(By.CSS_SELECTOR, '[data-testid="wcl-statistics"]')
    for category_div in categories_divs:
        try:
            category_name = category_div.find_element(By.CSS_SELECTOR, '[data-testid="wcl-statistics-category"]').text
            stat_values = [
                stat.text
                for stat in category_div.find_elements(By.CSS_SELECTOR, '[data-testid="wcl-statistics-value"]')
            ]
            statistics[category_name] = stat_values
        except Exception:
            print(Exception)
    return statistics


def change_url_to_statistics(url: str) -> str:
    new_url = url + "/game-statistics"
    return new_url


def get_completed_match_details(match_links):
    driver = webdriver.Chrome(service=service, options=options)
    output = {}
    try:
        for match_link in match_links:
            driver.get(match_link)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.tournamentHeader__country"))
            )

            match_summary = scrape_match_summary(driver)
            comment = match_summary["comment"]
            if comment == "CANCELLED":
                print("None")
                continue
            if comment.strip() and comment != "WALKOVER":
                driver.get(change_url_to_statistics(match_link))

                match_statistics = scrape_match_statistics(driver)

                match_data = {
                    "match_summary": match_summary,
                    "match_statistics": match_statistics,
                }
                output[match_link] = match_data


    except Exception as e:
        print(f"Error occurred: {e}")
        raise e

    finally:
        driver.quit()
    return output
