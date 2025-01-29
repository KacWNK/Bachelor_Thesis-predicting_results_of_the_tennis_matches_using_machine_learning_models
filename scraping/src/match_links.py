from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver_path = "C:\\chromedriver\\chromedriver.exe"

chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

options = Options()
options.binary_location = chrome_path

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

target_dates = ["JAN 24, FR", "JAN 25, SA", "JAN 26, SU", "JAN 27, MO", "JAN 28, TU", "TODAY", "JAN 30, TH"]


def get_match_links():
    completed_match_links = []
    scheduled_match_links = []
    try:
        for target_date in target_dates:

            driver.get("https://www.livesport.com/tennis/")
            calendar_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "calendarMenu"))
            )
            calendar_button.click()

            date_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "calendar__day"))
            )

            for date in date_elements:
                if date.text.strip() == target_date:
                    date.click()
                    break
            time.sleep(1)

            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "event__match"))
            )
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "event__titleBox"))
            )
            tournament_count = len(driver.find_elements(By.CLASS_NAME, "event__titleBox"))

            for i in range(tournament_count):
                while True:
                    try:
                        tournament = driver.find_elements(By.CLASS_NAME, "event__titleBox")[i]
                        tournament_name = tournament.text.strip()
                        if tournament_name and tournament_name.strip() != "":
                            break
                    except StaleElementReferenceException:
                        continue

                if not (
                        "atp" in tournament_name.lower() and "singles" in tournament_name.lower() and "qualification" not in tournament_name.lower()):
                    continue


                matches = []
                sibling = tournament.find_element(By.XPATH, "./ancestor::div[3]/following-sibling::*")
                while sibling:
                    if "event__match" in sibling.get_attribute("class"):
                        matches.append(sibling)
                        try:
                            sibling = sibling.find_element(By.XPATH, "following-sibling::*[1]")
                        except:
                            break
                    elif "event__titleBox" in sibling.get_attribute("class"):
                        break
                    else:
                        break

                for match in matches:
                    class_name = match.get_attribute("class")
                    if 'scheduled' not in class_name and 'live' not in class_name:
                        match_link_element = match.find_element(By.TAG_NAME, "a")
                        match_link = match_link_element.get_attribute("href")
                        completed_match_links.append(match_link)
                    elif 'scheduled' in class_name:
                        match_link_element = match.find_element(By.TAG_NAME, "a")
                        match_link = match_link_element.get_attribute("href")
                        scheduled_match_links.append(match_link)

    except Exception as e:
        print(f"Error occurred: {e}")
        raise e

    finally:
        driver.quit()
    return completed_match_links, scheduled_match_links
