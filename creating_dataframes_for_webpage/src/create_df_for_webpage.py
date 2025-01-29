import pandas as pd


def create_matches_df(processed_matches: pd.DataFrame, raw_matches: pd.DataFrame, match_predictions: pd.DataFrame):
    matches = pd.merge(processed_matches, match_predictions, on="match_id", how="left")
    matches = matches.drop(columns=['W1', 'W2', 'W3', 'W4', 'W5', 'L1', 'L2', 'L3', 'L4', 'L5'])
    matches = pd.merge(matches, raw_matches[['match_id', 'winner_seed', 'loser_seed', 'winner_entry', 'loser_entry',
                                             'W1', 'W2', 'W3', 'W4', 'W5', 'L1', 'L2', 'L3', 'L4', 'L5']],
                       on="match_id", how="inner")

    matches['Date'] = pd.to_datetime(matches['Date'])
    matches = matches.sort_values(by=['Date']).reset_index(drop=True)

    matches.loc[matches['true_label'] == 0, 'model_prediction'] = 1 - matches['model_prediction']
    matches.loc[matches['true_label'] == 0, 'odds_prediction'] = 1 - matches['odds_prediction']
    matches.rename({'model_prediction': 'winner_model_prediction', 'odds_prediction': 'winner_odds_prediction'},
                   axis='columns', inplace=True)
    matches = matches.drop(columns=['true_label'])
    matches['winner_rank_points'] = 2000
    matches['loser_rank_points'] = 2000

    if 'AvgW' not in list(matches.columns):
        matches['AvgW'] = 1.8
        matches['AvgL'] = 1.8

    matches_df = matches[[
        'match_id', 'Date', 'tournament_id', 'Round', 'indoor_or_outdoor', 'best_of', 'minutes', 'winner_id',
        'loser_id',
        'winner_seed', 'loser_seed', 'winner_entry', 'loser_entry', 'winner_rank', 'loser_rank', 'winner_rank_points',
        'loser_rank_points', 'winner_age', 'loser_age', 'W1', 'L1', 'W2', 'L2', 'W3', 'L3', 'W4', 'L4', 'W5', 'L5',
        'Wsets', 'Lsets', 'w_ace', 'l_ace', 'w_df', 'l_df', 'w_bpSaved', 'l_bpSaved', 'w_bpFaced', 'l_bpFaced',
        'w_svpt',
        'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon',
        'l_2ndWon', 'w_2ndIn', 'l_2ndIn', 'winner_1st_serve_in_pct', 'winner_1st_serve_win_pct',
        'winner_2nd_serve_in_pct', 'winner_2nd_serve_win_pct',
        'winner_service_games_won_pct', 'loser_1st_serve_in_pct', 'loser_1st_serve_win_pct', 'loser_2nd_serve_in_pct',
        'loser_2nd_serve_win_pct', 'loser_service_games_won_pct', 'winner_1st_serve_return_win_pct',
        'winner_2nd_serve_return_win_pct', 'winner_return_games_win_pct', 'loser_1st_serve_return_win_pct',
        'loser_2nd_serve_return_win_pct', 'loser_return_games_win_pct', 'winner_bp_won_pct', 'loser_bp_won_pct',
        'winner_bp_saved_pct', 'loser_bp_saved_pct', 'l_SvGms', 'Comment', 'AvgW', 'AvgL', 'winner_model_prediction',
        'winner_odds_prediction', 'uncertain', 'scheduled'
    ]]
    matches_df = matches_df.rename(columns={'Date': 'date'})

    return matches_df


def create_players_df(matches: pd.DataFrame):
    players_df = pd.concat([
        matches[['winner_id', 'winner_Name', 'winner_rank', 'winner_age', 'winner_hand']].rename(columns={
            'winner_id': 'player_id',
            'winner_Name': 'name',
            'winner_rank': 'rank',
            'winner_age': 'age',
            'winner_hand': 'hand'
        }),
        matches[['loser_id', 'loser_Name', 'loser_rank', 'loser_age', 'loser_hand']].rename(columns={
            'loser_id': 'player_id',
            'loser_Name': 'name',
            'loser_rank': 'rank',
            'loser_age': 'age',
            'loser_hand': 'hand'
        })
    ])

    players_df = players_df.drop_duplicates(subset=['player_id']).reset_index(drop=True)
    return players_df


def create_tournaments_df(matches: pd.DataFrame):
    tournaments_df = matches[
        [
            'tournament_id',
            'tournament_name',
            'tournament_location',
            'tournament_level',
            'Surface',
            'indoor_or_outdoor'
        ]
    ].drop_duplicates().reset_index(drop=True)
    return tournaments_df


def create_pre_match_stats_df(matches: pd.DataFrame):
    pre_match_stats_df = matches[['match_id',
                                  'w_ace_avg',
                                  'l_ace_avg',
                                  'w_CO_ace_avg',
                                  'l_CO_ace_avg',
                                  'w_df_avg',
                                  'l_df_avg',
                                  'w_CO_df_avg',
                                  'l_CO_df_avg',
                                  'w_2ndIn_avg',
                                  'l_2ndIn_avg',
                                  'w_CO_2ndIn_avg',
                                  'l_CO_2ndIn_avg',
                                  'winner_1st_serve_in_pct_avg',
                                  'loser_1st_serve_in_pct_avg',
                                  'winner_CO_1st_serve_in_pct_avg',
                                  'loser_CO_1st_serve_in_pct_avg',
                                  'winner_1st_serve_win_pct_avg',
                                  'loser_1st_serve_win_pct_avg',
                                  'winner_CO_1st_serve_win_pct_avg',
                                  'loser_CO_1st_serve_win_pct_avg',
                                  'winner_2nd_serve_in_pct_avg',
                                  'loser_2nd_serve_in_pct_avg',
                                  'winner_CO_2nd_serve_in_pct_avg',
                                  'loser_CO_2nd_serve_in_pct_avg',
                                  'winner_2nd_serve_win_pct_avg',
                                  'loser_2nd_serve_win_pct_avg',
                                  'winner_CO_2nd_serve_win_pct_avg',
                                  'loser_CO_2nd_serve_win_pct_avg',
                                  'winner_service_games_won_pct_avg',
                                  'loser_service_games_won_pct_avg',
                                  'winner_CO_service_games_won_pct_avg',
                                  'loser_CO_service_games_won_pct_avg',
                                  'winner_1st_serve_return_win_pct_avg',
                                  'loser_1st_serve_return_win_pct_avg',
                                  'winner_CO_1st_serve_return_win_pct_avg',
                                  'loser_CO_1st_serve_return_win_pct_avg',
                                  'winner_2nd_serve_return_win_pct_avg',
                                  'loser_2nd_serve_return_win_pct_avg',
                                  'winner_CO_2nd_serve_return_win_pct_avg',
                                  'loser_CO_2nd_serve_return_win_pct_avg',
                                  'winner_return_games_win_pct_avg',
                                  'loser_return_games_win_pct_avg',
                                  'winner_CO_return_games_win_pct_avg',
                                  'loser_CO_return_games_win_pct_avg',
                                  'winner_bp_won_pct_avg',
                                  'loser_bp_won_pct_avg',
                                  'winner_CO_bp_won_pct_avg',
                                  'loser_CO_bp_won_pct_avg',
                                  'winner_bp_saved_pct_avg',
                                  'loser_bp_saved_pct_avg',
                                  'winner_CO_bp_saved_pct_avg',
                                  'loser_CO_bp_saved_pct_avg',
                                  'non_CO_uncertainty',
                                  'CO_uncertainty',
                                  'elo_winner',
                                  'elo_loser',
                                  'surface_elo_winner',
                                  'surface_elo_loser',
                                  'blended_elo_winner',
                                  'blended_elo_loser',
                                  'winner_fatigue_score',
                                  'loser_fatigue_score',
                                  'winner_h2h_wins',
                                  'loser_h2h_wins',
                                  'winner_h2h_surface_wins',
                                  'loser_h2h_surface_wins',
                                  'tournament_country',
                                  'winner_home',
                                  'loser_home',
                                  'winner_injury_score',
                                  'loser_injury_score',
                                  'winner_win_pct_last_10',
                                  'loser_win_pct_last_10',
                                  'winner_win_pct_last_10_surface',
                                  'loser_win_pct_last_10_surface',
                                  'Round_Num',
                                  'Winner_Set_Diff_Tournament',
                                  'Winner_Game_Diff_Tournament',
                                  'Loser_Set_Diff_Tournament',
                                  'Loser_Game_Diff_Tournament',
                                  'winner_total_wins_tournament_history',
                                  'winner_total_losses_tournament_history',
                                  'loser_total_wins_tournament_history',
                                  'loser_total_losses_tournament_history']]
    return pre_match_stats_df


def create_df_for_webpage(processed_matches: pd.DataFrame, raw_matches: pd.DataFrame, match_predictions: pd.DataFrame):
    matches_df = create_matches_df(processed_matches, raw_matches, match_predictions)
    tournaments_df = create_tournaments_df(processed_matches)
    players_df = create_players_df(processed_matches)
    pre_match_stats_df = create_pre_match_stats_df(processed_matches)
    return matches_df, tournaments_df, players_df, pre_match_stats_df
