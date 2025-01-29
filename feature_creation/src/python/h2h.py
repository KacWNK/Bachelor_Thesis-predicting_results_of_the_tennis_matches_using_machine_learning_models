import pandas as pd


def add_h2h(new_rows: pd.DataFrame, existing_df: pd.DataFrame) -> pd.DataFrame:
    new_rows["Date"] = pd.to_datetime(new_rows["Date"], errors="coerce")
    if existing_df is not None:
        existing_df["Date"] = pd.to_datetime(existing_df["Date"], errors="coerce")

    if existing_df is not None:
        existing_df = existing_df.sort_values("Date").reset_index(drop=True)
    new_rows = new_rows.sort_values("Date").reset_index(drop=True)

    for i, row in new_rows.iterrows():
        winner, loser, surface, current_date = (
            row["winner_id"],
            row["loser_id"],
            row["Surface"],
            row["Date"],
        )

        if existing_df is not None and not existing_df.empty:
            general_existing = existing_df[
                (existing_df["winner_id"].isin([winner, loser])) &
                (existing_df["loser_id"].isin([winner, loser]))
                ]
        else:
            general_existing = pd.DataFrame()

        general_new = new_rows.iloc[:i][
            (new_rows.iloc[:i]["winner_id"].isin([winner, loser])) &
            (new_rows.iloc[:i]["loser_id"].isin([winner, loser]))
            ]

        previous_matches_general = pd.concat([general_existing, general_new], ignore_index=True)

        if not previous_matches_general.empty:
            previous_matches_general = previous_matches_general.sort_values("Date").drop_duplicates()

        if previous_matches_general is not None and not previous_matches_general.empty:
            last_match_general = previous_matches_general.iloc[-1]
            if last_match_general["winner_id"] == winner:
                prev_winner_h2h_wins = last_match_general["winner_h2h_wins"] + 1
                prev_loser_h2h_wins = last_match_general["loser_h2h_wins"]
            else:
                prev_winner_h2h_wins = last_match_general["loser_h2h_wins"] + 1
                prev_loser_h2h_wins = last_match_general["winner_h2h_wins"]
        else:
            prev_winner_h2h_wins = 0
            prev_loser_h2h_wins = 0

        previous_matches_surface = previous_matches_general[
            previous_matches_general["Surface"] == surface
            ] if previous_matches_general is not None else pd.DataFrame()

        if previous_matches_surface is not None and not previous_matches_surface.empty:
            last_match_surface = previous_matches_surface.iloc[-1]
            if last_match_surface["winner_id"] == winner:
                prev_winner_h2h_surface_wins = last_match_surface["winner_h2h_surface_wins"] + 1
                prev_loser_h2h_surface_wins = last_match_surface["loser_h2h_surface_wins"]
            else:
                prev_winner_h2h_surface_wins = last_match_surface["loser_h2h_surface_wins"] + 1
                prev_loser_h2h_surface_wins = last_match_surface["winner_h2h_surface_wins"]
        else:
            prev_winner_h2h_surface_wins = 0
            prev_loser_h2h_surface_wins = 0

        new_rows.at[i, "winner_h2h_wins"] = prev_winner_h2h_wins
        new_rows.at[i, "loser_h2h_wins"] = prev_loser_h2h_wins
        new_rows.at[i, "winner_h2h_surface_wins"] = prev_winner_h2h_surface_wins
        new_rows.at[i, "loser_h2h_surface_wins"] = prev_loser_h2h_surface_wins

    return new_rows

