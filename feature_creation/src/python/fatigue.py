import pandas as pd
from datetime import timedelta


def add_fatigue_scores(new_rows: pd.DataFrame, existing_df: pd.DataFrame) -> pd.DataFrame:
    combined_df = pd.concat([existing_df, new_rows], ignore_index=True) if existing_df is not None else new_rows
    combined_df = combined_df.drop_duplicates().reset_index(drop=True)
    combined_df['Date'] = pd.to_datetime(combined_df['Date'], errors='coerce')

    new_rows["winner_fatigue_score"] = 0.0
    new_rows["loser_fatigue_score"] = 0.0

    for i, row in new_rows.iterrows():
        current_date = pd.to_datetime(row["Date"])
        winner_id = row["winner_id"]
        loser_id = row["loser_id"]

        relevant_matches = combined_df[
            (combined_df["Date"] < current_date) &
            (combined_df["Date"] >= current_date - timedelta(days=7))
        ]

        winner_matches = relevant_matches[
            relevant_matches["winner_id"] == winner_id
        ]
        winner_fatigue = sum(
            0.85 ** ((current_date - match_date).days - 1) * minutes
            for match_date, minutes in zip(winner_matches["Date"], winner_matches["minutes"])
        )

        loser_matches = relevant_matches[
            relevant_matches["winner_id"] == loser_id
        ]
        loser_fatigue = sum(
            0.85 ** ((current_date - match_date).days - 1) * minutes
            for match_date, minutes in zip(loser_matches["Date"], loser_matches["minutes"])
        )

        new_rows.at[i, "winner_fatigue_score"] = winner_fatigue
        new_rows.at[i, "loser_fatigue_score"] = loser_fatigue

    return new_rows
