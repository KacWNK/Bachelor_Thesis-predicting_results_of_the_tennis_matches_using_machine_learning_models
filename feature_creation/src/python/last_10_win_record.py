import pandas as pd
import datetime


def calculate_win_percentage_before_match(new_rows: pd.DataFrame, existing_df: pd.DataFrame, player_id: str,
                                          current_date: datetime, surface=None):
    matches = pd.concat([existing_df, new_rows], ignore_index=True) if existing_df is not None else new_rows
    matches = matches.drop_duplicates().reset_index(drop=True)
    matches['Date'] = pd.to_datetime(matches['Date'], errors='coerce')

    # Filter matches for the given player before the current date
    player_matches = matches[
        ((matches['winner_id'] == player_id) | (matches['loser_id'] == player_id)) & (matches['Date'] < current_date)]

    if surface:
        player_matches = player_matches[player_matches['Surface'] == surface]

    player_matches = player_matches.sort_values(by='Date', ascending=False).head(10)

    total_matches = len(player_matches)
    if total_matches == 0:
        return 0.0

    wins = len(player_matches[player_matches['winner_id'] == player_id])
    return wins / total_matches


def add_last_10_win_record(new_rows: pd.DataFrame, existing_df: pd.DataFrame) -> pd.DataFrame:
    # Calculate win percentages
    new_rows['winner_win_pct_last_10'] = new_rows.apply(
        lambda row: calculate_win_percentage_before_match(new_rows, existing_df, row['winner_id'], row['Date']), axis=1)
    new_rows['loser_win_pct_last_10'] = new_rows.apply(
        lambda row: calculate_win_percentage_before_match(new_rows, existing_df, row['loser_id'], row['Date']), axis=1)
    new_rows['winner_win_pct_last_10_surface'] = new_rows.apply(
        lambda row: calculate_win_percentage_before_match(new_rows, existing_df, row['winner_id'], row['Date'],
                                                          row['Surface']), axis=1)
    new_rows['loser_win_pct_last_10_surface'] = new_rows.apply(
        lambda row: calculate_win_percentage_before_match(new_rows, existing_df, row['loser_id'], row['Date'],
                                                          row['Surface']), axis=1)

    return new_rows
