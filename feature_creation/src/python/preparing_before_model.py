import pandas as pd
import numpy as np


def prepare_before_model(matches: pd.DataFrame) -> pd.DataFrame:
    matches = matches.drop(
        columns=["W1", "L1", "W2", "L2", "W3", "L3", "W4", "L4", "W5", "L5", "Wsets", "Lsets", "tournament_location",
                 "tournament_name", "loser_id", "winner_id", "tournament_id", "draw_size", "tournament_date",
                 "winner_name", "winner_ioc", "winner_ht", "loser_name", "loser_ht", "loser_ioc", "winner_rank_points",
                 "loser_rank_points", "tournament_country", "Round", "time",
                 'minutes',
                 'w_ace',
                 'w_df',
                 'w_svpt',
                 'w_1stIn',
                 'w_1stWon',
                 'w_2ndWon',
                 'w_SvGms',
                 'w_bpSaved',
                 'w_bpFaced',
                 'l_ace',
                 'l_df',
                 'l_svpt',
                 'l_1stIn',
                 'l_1stWon',
                 'l_2ndWon',
                 'l_SvGms',
                 'l_bpSaved',
                 'l_bpFaced',
                 'Comment'
                 ], errors='ignore')


    matches['indoor_or_outdoor'] = matches['indoor_or_outdoor'].str.lower()
    matches['indoor_or_outdoor'] = matches['indoor_or_outdoor'].map({'outdoor': 1, 'indoor': 0})
    matches.rename(columns={'indoor_or_outdoor': 'outdoor'}, inplace=True)

    matches = pd.get_dummies(matches, columns=['Surface'], prefix='Surface')
    surfaces = ['clay', 'hard', 'grass']
    for surface in surfaces:
        column_name = f"Surface_{surface}"
        if column_name not in matches.columns:
            matches[column_name] = 0

    matches["tournament_level"] = matches["tournament_level"].map(
        {"ATP250": 0, "ATP500": 1, "Masters 1000": 3, "Grand Slam": 4, "ATP 250": 0, "ATP 500": 1})
    matches["winner_hand"] = matches["winner_hand"].map({"R": 1, "L": 0, "U": 0, "right": 1,
                                                         "left": 0})
    matches.rename(columns={'winner_hand': 'winner_right_handed'}, inplace=True)
    matches["loser_hand"] = matches["loser_hand"].map({"R": 1, "L": 0, "U": 0, "right": 1, "left": 0})
    matches.rename(columns={'loser_hand': 'loser_right_handed'}, inplace=True)
    matches["best_of"] = matches["best_of"].map({3: 1, 5: 0})
    matches['winner_age'] = matches['winner_age'].fillna(26.5)
    matches['loser_age'] = matches['loser_age'].fillna(26.5)

    def rename_player_columns(col):
        col_lower = col.lower()

        if col_lower.startswith('winner'):
            return col.replace('Winner', 'player1').replace('winner', 'player1')

        elif col_lower.startswith('loser'):
            return col.replace('Loser', 'player2').replace('loser', 'player2')

        elif col_lower.endswith('winner'):
            return f"player1_{col.replace('_winner', '').replace('Winner', '').replace('winner', '')}".strip('_')

        elif col_lower.endswith('loser'):
            return f"player2_{col.replace('_loser', '').replace('Loser', '').replace('loser', '')}".strip('_')

        return col

    matches.columns = [rename_player_columns(col) for col in list(matches.columns)]
    matches = matches.rename({"AvgW": 'player1_bet_odds', 'AvgL': 'player2_bet_odds'}, axis=1)
    matches = matches.astype({col: 'int64' for col in matches.select_dtypes(include=['bool']).columns})
    matches["target"] = 1
    matches = matches.copy()
    np.random.seed(42)
    rows_to_swap = np.random.choice(matches.index, size=int(len(matches) * 0.5), replace=False)

    for col in matches.columns:
        if col.startswith('player1_'):
            corresponding_col = col.replace('player1_', 'player2_')
            matches.loc[rows_to_swap, [col, corresponding_col]] = matches.loc[
                rows_to_swap, [corresponding_col, col]].values

        if col.endswith('_diff'):
            matches.loc[rows_to_swap, col] *= -1

    matches.loc[rows_to_swap, 'target'] = 0
    matches = matches.rename(
        columns={"Surface_clay": "Surface_Clay", "Surface_grass": "Surface_Grass", "Surface_hard": "Surface_Hard"})

    weather_data = pd.read_csv('feature_creation/data/created_features_separate/weather.csv')
    matches = matches.merge(weather_data, on='match_id', how='left')
    matches['temperature_2m'] = matches['temperature_2m'].fillna(24.5)
    matches['relative_humidity_2m'] = matches['relative_humidity_2m'].fillna(70)
    matches['windspeed_10m'] = matches['windspeed_10m'].fillna(10.1)
    matches['apparent_temperature'] = matches['apparent_temperature'].fillna(24.5)


    if 'player1_bet_odds' not in list(matches.columns):
        matches['player1_bet_odds'] = 1.8
        matches['player2_bet_odds'] = 1.8

    matches = matches[
        ['tournament_level', 'outdoor', 'player1_bet_odds', 'player2_bet_odds', 'match_id', 'player1_right_handed',
         'player1_age', 'player2_right_handed', 'player2_age', 'best_of', 'player1_rank', 'player2_rank',
         'player1_entry_LL', 'player1_entry_Q', 'player1_entry_WC', 'player2_entry_LL', 'player2_entry_Q',
         'player2_entry_WC', 'player1_is_seeded', 'player2_is_seeded', 'w_ace_avg', 'l_ace_avg', 'w_CO_ace_avg',
         'l_CO_ace_avg', 'w_df_avg', 'l_df_avg', 'w_CO_df_avg', 'l_CO_df_avg', 'w_2ndIn_avg', 'l_2ndIn_avg',
         'w_CO_2ndIn_avg', 'l_CO_2ndIn_avg', 'player1_1st_serve_in_pct_avg', 'player2_1st_serve_in_pct_avg',
         'player1_CO_1st_serve_in_pct_avg', 'player2_CO_1st_serve_in_pct_avg', 'player1_1st_serve_win_pct_avg',
         'player2_1st_serve_win_pct_avg', 'player1_CO_1st_serve_win_pct_avg', 'player2_CO_1st_serve_win_pct_avg',
         'player1_2nd_serve_in_pct_avg', 'player2_2nd_serve_in_pct_avg', 'player1_CO_2nd_serve_in_pct_avg',
         'player2_CO_2nd_serve_in_pct_avg', 'player1_2nd_serve_win_pct_avg', 'player2_2nd_serve_win_pct_avg',
         'player1_CO_2nd_serve_win_pct_avg', 'player2_CO_2nd_serve_win_pct_avg', 'player1_service_games_won_pct_avg',
         'player2_service_games_won_pct_avg', 'player1_CO_service_games_won_pct_avg',
         'player2_CO_service_games_won_pct_avg', 'player1_1st_serve_return_win_pct_avg',
         'player2_1st_serve_return_win_pct_avg', 'player1_CO_1st_serve_return_win_pct_avg',
         'player2_CO_1st_serve_return_win_pct_avg', 'player1_2nd_serve_return_win_pct_avg',
         'player2_2nd_serve_return_win_pct_avg', 'player1_CO_2nd_serve_return_win_pct_avg',
         'player2_CO_2nd_serve_return_win_pct_avg', 'player1_return_games_win_pct_avg',
         'player2_return_games_win_pct_avg',
         'player1_CO_return_games_win_pct_avg', 'player2_CO_return_games_win_pct_avg', 'player1_bp_won_pct_avg',
         'player2_bp_won_pct_avg', 'player1_CO_bp_won_pct_avg', 'player2_CO_bp_won_pct_avg', 'player1_bp_saved_pct_avg',
         'player2_bp_saved_pct_avg', 'player1_CO_bp_saved_pct_avg', 'player2_CO_bp_saved_pct_avg', 'non_CO_uncertainty',
         'CO_uncertainty', 'player1_elo', 'player2_elo', 'player1_surface_elo', 'player2_surface_elo',
         'player1_blended_elo', 'player2_blended_elo', 'player1_fatigue_score', 'player2_fatigue_score',
         'player1_h2h_wins',
         'player2_h2h_wins', 'player1_h2h_surface_wins', 'player2_h2h_surface_wins', 'player1_home', 'player2_home',
         'player1_injury_score', 'player2_injury_score', 'player1_win_pct_last_10', 'player2_win_pct_last_10',
         'player1_win_pct_last_10_surface', 'player2_win_pct_last_10_surface', 'Round_Num',
         'player1_Set_Diff_Tournament',
         'player1_Game_Diff_Tournament', 'player2_Set_Diff_Tournament', 'player2_Game_Diff_Tournament',
         'player1_total_wins_tournament_history', 'player1_total_losses_tournament_history',
         'player2_total_wins_tournament_history', 'player2_total_losses_tournament_history', 'temperature_2m',
         'relative_humidity_2m', 'windspeed_10m', 'apparent_temperature', 'Surface_Clay', 'Surface_Grass',
         'Surface_Hard',
         'target']]

    missing_values = matches.isnull().sum()

    columns_with_nan = missing_values[missing_values > 0]

    print("Columns with NaN values and their counts:")
    print(columns_with_nan)
    return matches
