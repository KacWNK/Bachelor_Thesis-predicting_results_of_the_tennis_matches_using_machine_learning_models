import pandas as pd
import subprocess

from scraping.src.match_links import get_match_links
from scraping.src.scrape_completed_matches import get_completed_match_details
from scraping.src.scrape_scheduled_matches import get_scheduled_match_details
from preprocessing.src.create_df_from_livesport_json import create_df_from_livesport
from feature_creation.main import process_new_data
from creating_dataframes_for_webpage.src.create_df_for_webpage import create_df_for_webpage


def load_data_to_django():
    try:
        subprocess.run(
            "cd tennis_bets_website && python manage.py update_load_data",
            shell=True,
            check=True,
        )
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    completed_match_links, scheduled_match_links = get_match_links()
    scheduled_match_details = get_scheduled_match_details(scheduled_match_links)
    completed_match_details = get_completed_match_details(completed_match_links)

    raw_scheduled_matches, new_scheduled_matches = create_df_from_livesport(scheduled_match_details, False)
    raw_completed_matches, new_completed_matches = create_df_from_livesport(completed_match_details, True)

    raw_matches = pd.concat([raw_scheduled_matches, raw_completed_matches], ignore_index=True)
    new_matches = pd.concat([new_scheduled_matches, new_completed_matches], ignore_index=True)

    existing_matches = pd.read_csv("main_flow/data/all_matches_processed.csv")
    existing_matches = existing_matches[~existing_matches['match_id'].isin(new_matches['match_id'])]
    updated_matches, new_matches_processed, predictions_net = process_new_data(new_matches, existing_matches)

    updated_matches.to_csv("main_flow/data/all_matches_processed.csv", index=False)

    matches_df, tournaments_df, players_df, pre_match_stats_df = create_df_for_webpage(new_matches_processed,
                                                                                       raw_matches, predictions_net)

    matches_df.to_csv("tennis_bets_website/stats/data/matches.csv")
    tournaments_df.to_csv("tennis_bets_website/stats/data/tournaments.csv")
    players_df.to_csv("tennis_bets_website/stats/data/players.csv")
    pre_match_stats_df.to_csv("tennis_bets_website/stats/data/pre-match_stats.csv")

    load_data_to_django()
