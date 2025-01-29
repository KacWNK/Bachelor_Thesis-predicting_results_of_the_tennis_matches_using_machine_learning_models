import pandas as pd

pd.set_option('future.no_silent_downcasting', True)


def check_tournament_stats_in_existing_df(df, player_id, tournament_id):
    if df is None:
        return {"sets": 0, "games": 0}

    filtered_df = df[
        ((df["winner_id"] == player_id) | (df["loser_id"] == player_id)) &
        (df["tournament_id"] == tournament_id)
        ]

    if filtered_df.empty:
        return {"sets": 0, "games": 0}

    latest_match = filtered_df.loc[filtered_df["Date"].idxmax()]
    if player_id == latest_match["winner_id"]:
        return {"sets": latest_match['Winner_Set_Diff_Tournament'],
                "games": latest_match['Winner_Game_Diff_Tournament']}
    else:
        return {"sets": latest_match['Loser_Set_Diff_Tournament'], "games": latest_match['Loser_Game_Diff_Tournament']}


def calculate_player_stats(new_rows: pd.DataFrame, existing_df: pd.DataFrame,
                           round_order: dict[str, int]) -> pd.DataFrame:
    new_rows['Round_Num'] = new_rows['Round'].map(round_order)
    new_rows = new_rows.sort_values(by=['Date', 'Round_Num'])
    player_stats = {}

    for index, row in new_rows.iterrows():
        winner_id = row['winner_id']
        loser_id = row['loser_id']
        tournament_id = row['tournament_id']

        if tournament_id not in player_stats:
            player_stats[tournament_id] = {}

        if winner_id not in player_stats[tournament_id]:
            player_stats[tournament_id][winner_id] = check_tournament_stats_in_existing_df(existing_df, winner_id,
                                                                                           tournament_id)
        if loser_id not in player_stats[tournament_id]:
            player_stats[tournament_id][loser_id] = check_tournament_stats_in_existing_df(existing_df, loser_id,
                                                                                          tournament_id)

        new_rows.at[index, 'Winner_Set_Diff_Tournament'] = player_stats[tournament_id][winner_id]['sets']
        new_rows.at[index, 'Winner_Game_Diff_Tournament'] = player_stats[tournament_id][winner_id]['games']
        new_rows.at[index, 'Loser_Set_Diff_Tournament'] = player_stats[tournament_id][loser_id]['sets']
        new_rows.at[index, 'Loser_Game_Diff_Tournament'] = player_stats[tournament_id][loser_id]['games']

        winner_sets = int(row['Wsets']) if pd.notna(row['Wsets']) else 0
        loser_sets = int(row['Lsets']) if pd.notna(row['Lsets']) else 0

        winner_gems = sum(row[['W1', 'W2', 'W3', 'W4', 'W5']].fillna(0).values[:(winner_sets + loser_sets)])
        loser_gems = sum(row[['L1', 'L2', 'L3', 'L4', 'L5']].fillna(0).values[:(winner_sets + loser_sets)])

        player_stats[tournament_id][winner_id]['sets'] += (winner_sets - loser_sets)
        player_stats[tournament_id][winner_id]['games'] += (winner_gems - loser_gems)

        player_stats[tournament_id][loser_id]['sets'] += (loser_sets - winner_sets)
        player_stats[tournament_id][loser_id]['games'] += (loser_gems - winner_gems)

    return new_rows


def add_current_tournament_stats(new_rows: pd.DataFrame, existing_df: pd.DataFrame) -> pd.DataFrame:
    round_order = {
        '1st Round': 1,
        '2nd Round': 2,
        '3rd Round': 3,
        '4th Round': 4,
        'Quarterfinals': 5,
        'Semifinals': 6,
        'The Final': 7
    }

    new_rows = calculate_player_stats(new_rows, existing_df, round_order)

    return new_rows
