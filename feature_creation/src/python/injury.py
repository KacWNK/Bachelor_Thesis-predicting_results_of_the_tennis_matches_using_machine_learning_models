import pandas as pd


def check_injury_in_existing_df(df, player_id):
    if df is None:
        return 0
    filtered_df = df[
        (df["winner_id"] == player_id) | (df["loser_id"] == player_id)
        ].sort_values("Date", ascending=False)

    if filtered_df.empty:
        return 0

    latest_match = filtered_df.iloc[0]

    if latest_match["loser_id"] == player_id and latest_match["Comment"] == "Retired":
        return 1
    else:
        return 0


def add_injury(new_rows: pd.DataFrame, existing_df: pd.DataFrame) -> pd.DataFrame:
    new_rows = new_rows.sort_values(by=['Date'])

    last_match_retired = {}
    
    for idx, row in new_rows.iterrows():
        winner_id = row['winner_id']
        loser_id = row['loser_id']

        if winner_id in last_match_retired:
            if last_match_retired[winner_id] == 1:
                new_rows.at[idx, 'winner_injury_score'] = 1
            else:
                new_rows.at[idx, 'winner_injury_score'] = 0
        else:
            new_rows.at[idx, 'winner_injury_score'] = check_injury_in_existing_df(existing_df, winner_id)

        if loser_id in last_match_retired:
            if last_match_retired[loser_id] == 1:
                new_rows.at[idx, 'loser_injury_score'] = 1
            else:
                new_rows.at[idx, 'loser_injury_score'] = 0
        else:
            new_rows.at[idx, 'loser_injury_score'] = check_injury_in_existing_df(existing_df, winner_id)

        if row['Comment'] == 'Retired':  
            last_match_retired[loser_id] = 1
        else:
            last_match_retired[loser_id] = 0

        last_match_retired[winner_id] = 0
    return new_rows
