from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

driver_path = "C:\\chromedriver\\chromedriver.exe"

chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

# Set Chrome options
options = Options()
options.binary_location = chrome_path

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)
match_links = []

try:
    url = "https://www.livesport.com/en/tennis/calendar/atp/"
    driver.get(url)

    # Wait for the dynamic content to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "seasonCalendar__container"))
    )

    calendar_container = driver.find_element(By.CLASS_NAME, "seasonCalendar__container")
    calendar_items = calendar_container.find_elements(By.CLASS_NAME, "seasonCalendar__content")

    i = 0
    for item in calendar_items:

        try:
            month_year = item.find_element(By.CLASS_NAME, "seasonCalendar__headline").text.strip()

            rows = item.find_elements(By.CLASS_NAME, "seasonCalendar__row")
            for row in rows:
                date = row.find_element(By.CLASS_NAME, "seasonCalendar__date").text.strip()

                tournament_link_element = row.find_element(By.CLASS_NAME, "seasonCalendar__name").find_element(
                    By.TAG_NAME, "a")
                tournament_name = tournament_link_element.text.strip()
                tournament_link = f"{tournament_link_element.get_attribute('href')}/results"

                try:
                    winner_element = row.find_element(By.CLASS_NAME, "seasonCalendar__winner").find_element(By.TAG_NAME,
                                                                                                            "a")
                    winner = winner_element.text.strip()
                except:
                    winner = "No winner listed"
                print(tournament_link)
                driver.get(tournament_link)
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "event__match"))
                )

                match_divs = driver.find_elements(By.CLASS_NAME, "event__match")

                matches = []

                for match_div in match_divs:
                    try:
                        match_link_element = match_div.find_element(By.TAG_NAME, "a")
                        match_link = match_link_element.get_attribute("href")
                        print(match_link)
                        match_links.append(match_link)
                    except Exception as e:
                        print(f"Error processing match div: {e}")

                # Go back to the calendar page
                driver.back()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "seasonCalendar__container"))
                )

        except Exception as e:
            print(f"Error processing item: {e}")


finally:
    with open("../../data/livesport_scraped/match_links_2024.json", "w") as file:
        json.dump(match_links, file, indent=4)
    driver.quit()
