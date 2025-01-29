import pandas as pd
import numpy as np
from scipy.stats import entropy


def calculate_1st_serve_in_percentage(row):
    if pd.isna(row['w_svpt']) or pd.isna(row['w_1stIn']):
        return None
    if row['w_svpt'] > 0:
        return row['w_1stIn'] / row['w_svpt']
    return 0


def calculate_1st_serve_win_percentage(row):
    if pd.isna(row['w_1stIn']) or pd.isna(row['w_1stWon']):
        return None
    if row['w_1stIn'] > 0:
        return row['w_1stWon'] / row['w_1stIn']
    return 0


def calculate_2nd_serve_in_percentage(row):
    if pd.isna(row['w_svpt']) or pd.isna(row['w_2ndIn']):
        return None
    if row['w_svpt'] - row['w_1stIn'] > 0:
        return row['w_2ndIn'] / (row['w_svpt'] - row['w_1stIn'])
    return 0


def calculate_2nd_serve_win_percentage(row):
    if pd.isna(row['w_2ndIn']) or pd.isna(row['w_2ndWon']):
        return None
    if row['w_svpt'] - row['w_1stIn'] > 0:
        return row['w_2ndWon'] / (row['w_svpt'] - row['w_1stIn'])
    return 0


def calculate_service_games_won_percentage(row):
    if pd.isna(row['w_SvGms']) or pd.isna(row['w_bpFaced']) or pd.isna(row['w_bpSaved']):
        return None
    if row['w_SvGms'] > 0:
        return (row['w_SvGms'] - (row['w_bpFaced'] - row['w_bpSaved'])) / row['w_SvGms']
    return 0


def calculate_1st_serve_in_percentage_loser(row):
    if pd.isna(row['l_svpt']) or pd.isna(row['l_1stIn']):
        return None
    if row['l_svpt'] > 0:
        return row['l_1stIn'] / row['l_svpt']
    return 0


def calculate_1st_serve_win_percentage_loser(row):
    if pd.isna(row['l_1stIn']) or pd.isna(row['l_1stWon']):
        return None
    if row['l_1stIn'] > 0:
        return row['l_1stWon'] / row['l_1stIn']
    return 0


def calculate_2nd_serve_in_percentage_loser(row):
    if pd.isna(row['l_svpt']) or pd.isna(row['l_1stIn']) or pd.isna(row['l_2ndIn']):
        return None
    if row['l_svpt'] - row['l_1stIn'] > 0:
        return row['l_2ndIn'] / (row['l_svpt'] - row['l_1stIn'])
    return 0


def calculate_2nd_serve_win_percentage_loser(row):
    if pd.isna(row['l_2ndIn']) or pd.isna(row['l_2ndWon']):
        return None
    if row['l_svpt'] - row['l_1stIn'] > 0:
        return row['l_2ndWon'] / (row['l_svpt'] - row['l_1stIn'])
    return 0


def calculate_service_games_won_percentage_loser(row):
    if pd.isna(row['l_SvGms']) or pd.isna(row['l_bpFaced']) or pd.isna(row['l_bpSaved']):
        return None
    if row['l_SvGms'] > 0:
        return (row['l_SvGms'] - (row['l_bpFaced'] - row['l_bpSaved'])) / row['l_SvGms']
    return 0


def add_player_match_stats(matches: pd.DataFrame) -> pd.DataFrame:
    matches['winner_1st_serve_in_pct'] = matches.apply(calculate_1st_serve_in_percentage, axis=1)
    matches['winner_1st_serve_win_pct'] = matches.apply(calculate_1st_serve_win_percentage, axis=1)
    matches['winner_2nd_serve_in_pct'] = matches.apply(calculate_2nd_serve_in_percentage, axis=1)
    matches['winner_2nd_serve_win_pct'] = matches.apply(calculate_2nd_serve_win_percentage, axis=1)
    matches['winner_service_games_won_pct'] = matches.apply(calculate_service_games_won_percentage, axis=1)
    matches['loser_1st_serve_in_pct'] = matches.apply(calculate_1st_serve_in_percentage_loser, axis=1)
    matches['loser_1st_serve_win_pct'] = matches.apply(calculate_1st_serve_win_percentage_loser, axis=1)
    matches['loser_2nd_serve_in_pct'] = matches.apply(calculate_2nd_serve_in_percentage_loser, axis=1)
    matches['loser_2nd_serve_win_pct'] = matches.apply(calculate_2nd_serve_win_percentage_loser, axis=1)
    matches['loser_service_games_won_pct'] = matches.apply(calculate_service_games_won_percentage_loser, axis=1)

    return matches


def calculate_1st_serve_return_win_percentage(row):
    if pd.isna(row['loser_1st_serve_win_pct']):
        return None
    return 1 - row['loser_1st_serve_win_pct']


def calculate_2nd_serve_return_win_percentage(row):
    if pd.isna(row['loser_2nd_serve_win_pct']):
        return None
    return 1 - row['loser_2nd_serve_win_pct']


def calculate_return_games_win_percentage(row):
    if pd.isna(row['loser_service_games_won_pct']):
        return None
    return 1 - row['loser_service_games_won_pct']


def calculate_1st_serve_return_win_percentage_loser(row):
    if pd.isna(row['winner_1st_serve_win_pct']):
        return None
    return 1 - row['winner_1st_serve_win_pct']


def calculate_2nd_serve_return_win_percentage_loser(row):
    if pd.isna(row['winner_2nd_serve_win_pct']):
        return None
    return 1 - row['winner_2nd_serve_win_pct']


def calculate_return_games_win_percentage_loser(row):
    if pd.isna(row['winner_service_games_won_pct']):
        return None
    return 1 - row['winner_service_games_won_pct']


def add_player_match_stats_2(matches: pd.DataFrame) -> pd.DataFrame:
    matches['winner_1st_serve_return_win_pct'] = matches.apply(calculate_1st_serve_return_win_percentage, axis=1)
    matches['winner_2nd_serve_return_win_pct'] = matches.apply(calculate_2nd_serve_return_win_percentage, axis=1)
    matches['winner_return_games_win_pct'] = matches.apply(calculate_return_games_win_percentage, axis=1)
    matches['loser_1st_serve_return_win_pct'] = matches.apply(calculate_1st_serve_return_win_percentage_loser, axis=1)
    matches['loser_2nd_serve_return_win_pct'] = matches.apply(calculate_2nd_serve_return_win_percentage_loser, axis=1)
    matches['loser_return_games_win_pct'] = matches.apply(calculate_return_games_win_percentage_loser, axis=1)

    return matches


def calculate_percentage_of_break_points_won_on_opponents_serve(row):
    if pd.isna(row['l_bpFaced']) or pd.isna(row['l_bpSaved']):
        return None
    if row['l_bpFaced'] > 0:
        return (row['l_bpFaced'] - row['l_bpSaved']) / row['l_bpFaced']
    return 0


def calculate_percentage_of_break_points_won_on_opponents_serve_loser(row):
    if pd.isna(row['w_bpFaced']) or pd.isna(row['w_bpSaved']):
        return None
    if row['w_bpFaced'] > 0:
        return (row['w_bpFaced'] - row['w_bpSaved']) / row['w_bpFaced']
    return 0


def calculate_percentage_of_break_points_saved(row):
    if pd.isna(row['w_bpFaced']) or pd.isna(row['w_bpSaved']):
        return None
    if row['w_bpFaced'] > 0:
        return row['w_bpSaved'] / row['w_bpFaced']
    return 0


def calculate_percentage_of_break_points_saved_loser(row):
    if pd.isna(row['l_bpFaced']) or pd.isna(row['l_bpSaved']):
        return None
    if row['l_bpFaced'] > 0:
        return row['l_bpSaved'] / row['l_bpFaced']
    return 0


def add_player_match_stats_3(matches: pd.DataFrame) -> pd.DataFrame:
    matches['winner_bp_won_pct'] = matches.apply(calculate_percentage_of_break_points_won_on_opponents_serve, axis=1)
    matches['loser_bp_won_pct'] = matches.apply(calculate_percentage_of_break_points_won_on_opponents_serve_loser,
                                                axis=1)
    matches['winner_bp_saved_pct'] = matches.apply(calculate_percentage_of_break_points_saved, axis=1)
    matches['loser_bp_saved_pct'] = matches.apply(calculate_percentage_of_break_points_saved_loser, axis=1)

    return matches


def calculate_surface_weights_kl(data, stat_cols, surface_col, bins=20, handle_nans='fill'):
    weights_dict = {}
    surfaces = data[surface_col].unique()
    winner_cols = [col for col in stat_cols if col.startswith('w')]
    loser_cols = [col for col in stat_cols if col.startswith('l')]

    for winner_col, loser_col in zip(winner_cols, loser_cols):
        if handle_nans == 'fill':
            data[winner_col] = data[winner_col].fillna(data[winner_col].mean())
            data[loser_col] = data[loser_col].fillna(data[loser_col].mean())
        elif handle_nans == 'skip':
            data = data.dropna(subset=[winner_col, loser_col])

        weights = pd.DataFrame(0.0, index=surfaces, columns=surfaces)

        for s1 in surfaces:
            for s2 in surfaces:
                p_data = np.concatenate([
                    data[data[surface_col] == s1][winner_col].values,
                    data[data[surface_col] == s1][loser_col].values
                ])
                q_data = np.concatenate([
                    data[data[surface_col] == s2][winner_col].values,
                    data[data[surface_col] == s2][loser_col].values
                ])

                p_hist, bin_edges = np.histogram(p_data, bins=bins, density=True)
                q_hist, _ = np.histogram(q_data, bins=bin_edges, density=True)

                p_hist = p_hist + 1e-9
                q_hist = q_hist + 1e-9

                p_hist /= p_hist.sum()
                q_hist /= q_hist.sum()

                kl_div = entropy(p_hist, q_hist)
                weights.loc[s1, s2] = 1 / (1 + kl_div)

        weights_dict[winner_col] = weights
        weights_dict[loser_col] = weights

    return weights_dict


def number_of_common_opponent_matches(row, df):
    player_a = row['winner_id']
    player_b = row['loser_id']
    current_date = row['Date']

    df = df[df['Date'] < current_date]

    player_a_opponents = set(df[(df['winner_id'] == player_a)]['loser_id']).union(
        set(df[(df['loser_id'] == player_a)]['winner_id']))
    player_b_opponents = set(df[(df['winner_id'] == player_b)]['loser_id']).union(
        set(df[(df['loser_id'] == player_b)]['winner_id']))

    common_opponents = player_a_opponents.intersection(player_b_opponents)
    return len(common_opponents)


def calculate_weighted_mean(values, times, surface_weights, decay_rate=0.3):
    if len(values) == 0 or len(times) == 0:
        return 0.0
    time_weights = np.exp(-decay_rate * times)
    combined_weights = surface_weights * time_weights
    return np.sum(combined_weights * values) / np.sum(combined_weights)


def calculate_uncertainty_from_weights(values, times, surface_weights, decay_rate=0.3):
    if len(values) == 0 or len(times) == 0:
        return 1.0

    time_weights = np.exp(-decay_rate * times)
    combined_weights = surface_weights * time_weights

    total_weight = np.sum(combined_weights)

    uncertainty = 1 / total_weight if total_weight > 0 else 1.0

    return uncertainty


def calculate_stats_with_uncertainty(row, df, weights_dict, winner_col, loser_col, surface_col, time_decay=0.3,
                                     is_co=False):
    player_a = row['winner_id']
    player_b = row['loser_id']
    current_date = row['Date']
    current_surface = row[surface_col]

    past_matches = df[df['Date'] < current_date].copy()
    if is_co:
        player_a_opponents = set(past_matches[past_matches['winner_id'] == player_a]['loser_id']).union(
            past_matches[past_matches['loser_id'] == player_a]['winner_id']
        )
        player_b_opponents = set(past_matches[past_matches['winner_id'] == player_b]['loser_id']).union(
            past_matches[past_matches['loser_id'] == player_b]['winner_id']
        )
        common_opponents = player_a_opponents.intersection(player_b_opponents)
        past_matches = past_matches[
            (
                    (past_matches['winner_id'].isin(common_opponents)) | (
                past_matches['loser_id'].isin(common_opponents))
            )
        ]

    past_matches['time_since_match'] = (current_date - past_matches['Date']).dt.days / 365.0

    player_a_matches = past_matches[
        (past_matches['winner_id'] == player_a) | (past_matches['loser_id'] == player_a)
        ]
    player_a_stats = player_a_matches[winner_col].combine_first(player_a_matches[loser_col]).fillna(0)
    player_a_times = player_a_matches['time_since_match']

    player_b_matches = past_matches[
        (past_matches['winner_id'] == player_b) | (past_matches['loser_id'] == player_b)
        ]
    player_b_stats = player_b_matches[winner_col].combine_first(player_b_matches[loser_col]).fillna(0)
    player_b_times = player_b_matches['time_since_match']

    player_a_surfaces = player_a_matches[surface_col].values
    player_a_surface_weights = np.array([
        weights_dict[winner_col].loc[current_surface, surface] for surface in player_a_surfaces
    ])
    player_b_surfaces = player_b_matches[surface_col].values
    player_b_surface_weights = np.array([
        weights_dict[winner_col].loc[current_surface, surface] for surface in player_b_surfaces
    ])

    player_a_mean = calculate_weighted_mean(
        player_a_stats.values, player_a_times.values, player_a_surface_weights, time_decay
    )
    player_b_mean = calculate_weighted_mean(
        player_b_stats.values, player_b_times.values, player_b_surface_weights, time_decay
    )

    player_a_uncertainty = calculate_uncertainty_from_weights(player_a_stats.values, player_a_times.values,
                                                              player_a_surface_weights, time_decay)
    player_b_uncertainty = calculate_uncertainty_from_weights(player_b_stats.values, player_b_times.values,
                                                              player_b_surface_weights, time_decay)

    return player_a_mean, player_b_mean, player_a_uncertainty, player_b_uncertainty


def process_all_stats(new_matches: pd.DataFrame, existing_df: pd.DataFrame, weights_dict, stat_cols: [tuple],
                      surface_col):
    results = {}
    for stat_tuple in stat_cols:
        winner_col = stat_tuple[0]
        loser_col = stat_tuple[1]

        means_uncertainties = new_matches.apply(
            lambda row: calculate_stats_with_uncertainty(
                row, existing_df, weights_dict, winner_col, loser_col, surface_col, is_co=False
            ),
            axis=1,
        )
        winner_avg, loser_avg, winner_unc, loser_unc = zip(*means_uncertainties)

        results[f"{winner_col}_avg"] = winner_avg
        results[f"{loser_col}_avg"] = loser_avg
        results[f"{winner_col}_uncertainty"] = winner_unc
        results[f"{loser_col}_uncertainty"] = loser_unc

        co_means_uncertainties = new_matches.apply(
            lambda row: calculate_stats_with_uncertainty(
                row, existing_df, weights_dict, winner_col, loser_col, surface_col, is_co=True
            ),
            axis=1,
        )
        co_winner_avg, co_loser_avg, co_winner_unc, co_loser_unc = zip(*co_means_uncertainties)

        if winner_col.startswith('w_'):
            results[f"{winner_col.replace('w', 'w_CO')}_avg"] = co_winner_avg
            results[f"{loser_col.replace('l', 'l_CO')}_avg"] = co_loser_avg
            results[f"{winner_col.replace('w', 'w_CO')}_uncertainty"] = co_winner_unc
            results[f"{loser_col.replace('l', 'l_CO')}_uncertainty"] = co_loser_unc
        if winner_col.startswith('winner'):
            results[f"{winner_col.replace('winner', 'winner_CO')}_avg"] = co_winner_avg
            results[f"{loser_col.replace('loser', 'loser_CO')}_avg"] = co_loser_avg
            results[f"{winner_col.replace('winner', 'winner_CO')}_uncertainty"] = co_winner_unc
            results[f"{loser_col.replace('loser', 'loser_CO')}_uncertainty"] = co_loser_unc

    for col, values in results.items():
        new_matches[col] = values

    return new_matches


def calculate_combined_uncertainties(df, stat_cols: [tuple]):
    non_co_uncertainty_cols_winner = []
    non_co_uncertainty_cols_loser = []
    co_uncertainty_cols_winner = []
    co_uncertainty_cols_loser = []
    for stat_tuple in stat_cols:
        winner_col = stat_tuple[0]
        loser_col = stat_tuple[1]

        non_co_uncertainty_cols_winner.append(f"{winner_col}_uncertainty")
        non_co_uncertainty_cols_loser.append(f"{loser_col}_uncertainty")

        if winner_col.startswith('w_'):
            co_uncertainty_cols_winner.append(f"{winner_col.replace('w', 'w_CO')}_uncertainty")
            co_uncertainty_cols_loser.append(f"{loser_col.replace('l', 'l_CO')}_uncertainty")
        if winner_col.startswith('winner'):
            co_uncertainty_cols_winner.append(f"{winner_col.replace('winner', 'winner_CO')}_uncertainty")
            co_uncertainty_cols_loser.append(f"{loser_col.replace('loser', 'loser_CO')}_uncertainty")

    df['non_CO_uncertainty_winner'] = df[non_co_uncertainty_cols_winner].mean(axis=1)
    df['CO_uncertainty_winner'] = df[co_uncertainty_cols_winner].mean(axis=1)
    df['non_CO_uncertainty_loser'] = df[non_co_uncertainty_cols_loser].mean(axis=1)
    df['CO_uncertainty_loser'] = df[co_uncertainty_cols_loser].mean(axis=1)
    return df


def add_aggregated_player_stats(new_rows: pd.DataFrame, existing_df: pd.DataFrame) -> pd.DataFrame:
    new_rows = new_rows.sort_values(by='Date')

    new_rows['w_2ndIn'] = new_rows['w_svpt'] - new_rows['w_1stIn'] - new_rows['w_df']
    new_rows['l_2ndIn'] = new_rows['l_svpt'] - new_rows['l_1stIn'] - new_rows['l_df']

    new_rows = add_player_match_stats(new_rows)
    new_rows = add_player_match_stats_2(new_rows)
    new_rows = add_player_match_stats_3(new_rows)

    new_rows[['num_CO_matches']] = new_rows.apply(
        lambda row: pd.Series(number_of_common_opponent_matches(row, new_rows)), axis=1
    )

    matches = pd.concat([existing_df, new_rows], ignore_index=True) if existing_df is not None else new_rows
    matches = matches.drop_duplicates().reset_index(drop=True)
    matches['Date'] = pd.to_datetime(matches['Date'], errors='coerce')
    matches = matches.sort_values(by='Date')

    weights_dict = calculate_surface_weights_kl(matches, ['w_ace', 'l_ace', 'w_df', 'l_df', 'w_2ndIn', 'l_2ndIn',
                                                          'winner_1st_serve_in_pct',
                                                          'winner_1st_serve_win_pct',
                                                          'winner_2nd_serve_in_pct',
                                                          'winner_2nd_serve_win_pct',
                                                          'winner_service_games_won_pct',
                                                          'loser_1st_serve_in_pct',
                                                          'loser_1st_serve_win_pct',
                                                          'loser_2nd_serve_in_pct',
                                                          'loser_2nd_serve_win_pct',
                                                          'loser_service_games_won_pct',
                                                          'winner_1st_serve_return_win_pct',
                                                          'winner_2nd_serve_return_win_pct',
                                                          'winner_return_games_win_pct',
                                                          'loser_1st_serve_return_win_pct',
                                                          'loser_2nd_serve_return_win_pct',
                                                          'loser_return_games_win_pct',
                                                          'winner_bp_won_pct',
                                                          'loser_bp_won_pct',
                                                          'winner_bp_saved_pct',
                                                          'loser_bp_saved_pct'], 'Surface', bins=20)

    new_rows = process_all_stats(new_rows, matches, weights_dict, [('w_ace', 'l_ace'), ('w_df', 'l_df'),
                                                                   ('w_2ndIn', 'l_2ndIn'),
                                                                   (
                                                                       'winner_1st_serve_in_pct',
                                                                       'loser_1st_serve_in_pct'),
                                                                   ('winner_1st_serve_win_pct',
                                                                    'loser_1st_serve_win_pct'),
                                                                   (
                                                                       'winner_2nd_serve_in_pct',
                                                                       'loser_2nd_serve_in_pct'),
                                                                   ('winner_2nd_serve_win_pct',
                                                                    'loser_2nd_serve_win_pct'),
                                                                   ('winner_service_games_won_pct',
                                                                    'loser_service_games_won_pct'),
                                                                   ('winner_1st_serve_return_win_pct',
                                                                    'loser_1st_serve_return_win_pct'),
                                                                   ('winner_2nd_serve_return_win_pct',
                                                                    'loser_2nd_serve_return_win_pct'),
                                                                   ('winner_return_games_win_pct',
                                                                    'loser_return_games_win_pct'),
                                                                   ('winner_bp_won_pct', 'loser_bp_won_pct'),
                                                                   ('winner_bp_saved_pct', 'loser_bp_saved_pct')
                                                                   ]
                                 , 'Surface')

    new_rows = new_rows.copy()
    new_rows = calculate_combined_uncertainties(new_rows, [('w_ace', 'l_ace'), ('w_df', 'l_df'),
                                                           ('w_2ndIn', 'l_2ndIn'),
                                                           ('winner_1st_serve_in_pct', 'loser_1st_serve_in_pct'),
                                                           ('winner_1st_serve_win_pct', 'loser_1st_serve_win_pct'),
                                                           ('winner_2nd_serve_in_pct', 'loser_2nd_serve_in_pct'),
                                                           ('winner_2nd_serve_win_pct', 'loser_2nd_serve_win_pct'),
                                                           ('winner_service_games_won_pct',
                                                            'loser_service_games_won_pct'),
                                                           ('winner_1st_serve_return_win_pct',
                                                            'loser_1st_serve_return_win_pct'),
                                                           ('winner_2nd_serve_return_win_pct',
                                                            'loser_2nd_serve_return_win_pct'),
                                                           (
                                                               'winner_return_games_win_pct',
                                                               'loser_return_games_win_pct'),
                                                           ('winner_bp_won_pct', 'loser_bp_won_pct'),
                                                           ('winner_bp_saved_pct', 'loser_bp_saved_pct')
                                                           ])

    new_rows["CO_uncertainty_winner"] = new_rows["CO_uncertainty_winner"].clip(lower=0, upper=1)
    new_rows["CO_uncertainty_loser"] = new_rows["CO_uncertainty_loser"].clip(lower=0, upper=1)
    new_rows["non_CO_uncertainty_winner"] = new_rows["non_CO_uncertainty_winner"].clip(lower=0, upper=1)
    new_rows["CO_uncertainty_loser"] = new_rows["CO_uncertainty_loser"].clip(lower=0, upper=1)

    new_rows["CO_uncertainty"] = np.sqrt(new_rows["CO_uncertainty_winner"] * new_rows["CO_uncertainty_loser"])
    new_rows["non_CO_uncertainty"] = np.sqrt(
        new_rows["non_CO_uncertainty_winner"] * new_rows["non_CO_uncertainty_loser"])

    return new_rows
