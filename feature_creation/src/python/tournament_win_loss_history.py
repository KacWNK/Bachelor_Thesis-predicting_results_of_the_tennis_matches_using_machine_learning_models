import pandas as pd


def check_tournament_stats_in_existing_df(df, player_id, tournament_location) -> tuple[int, int]:
    if df is None:
        return 0, 0

    filtered_df = df[
        ((df["winner_id"] == player_id) | (df["loser_id"] == player_id)) &
        (df["tournament_location"].str.lower() == tournament_location.lower())
        ]

    if filtered_df.empty:
        return 0, 0

    latest_match = filtered_df.loc[filtered_df["Date"].idxmax()]
    if player_id == latest_match["winner_id"]:
        return latest_match['winner_total_wins_tournament_history'] + 1, latest_match['winner_total_losses_tournament_history']
    else:
        return latest_match['loser_total_wins_tournament_history'], latest_match['loser_total_losses_tournament_history'] + 1


def add_tournament_win_loss_history(new_matches: pd.DataFrame, existing_df: pd.DataFrame) -> pd.DataFrame:
    new_matches = new_matches.sort_values(by='Date')

    player_stats = {}

    for i, row in new_matches.iterrows():
        tournament = row['tournament_location'].lower()
        winner_id = row['winner_id']
        loser_id = row['loser_id']
        if tournament not in player_stats:
            player_stats[tournament] = {}

        if winner_id not in player_stats[tournament]:
            winner_stats = check_tournament_stats_in_existing_df(existing_df, winner_id, tournament)
            player_stats[tournament][winner_id] = {'wins': winner_stats[0], 'losses': winner_stats[1]}
        if loser_id not in player_stats[tournament]:
            loser_stats = check_tournament_stats_in_existing_df(existing_df, loser_id, tournament)
            player_stats[tournament][loser_id] = {'wins': loser_stats[0], 'losses': loser_stats[1]}

        new_matches.at[i, 'winner_total_wins_tournament_history'] = player_stats[tournament][winner_id]['wins']
        new_matches.at[i, 'winner_total_losses_tournament_history'] = player_stats[tournament][winner_id]['losses']
        new_matches.at[i, 'loser_total_wins_tournament_history'] = player_stats[tournament][loser_id]['wins']
        new_matches.at[i, 'loser_total_losses_tournament_history'] = player_stats[tournament][loser_id]['losses']

        player_stats[tournament][winner_id]['wins'] += 1
        player_stats[tournament][loser_id]['losses'] += 1

    return new_matches
