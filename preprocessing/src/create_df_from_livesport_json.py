import pandas as pd
import json
import numpy as np
import re
from datetime import datetime
import random


def create_df_from_livesport(livesport, completed: bool):
    if livesport == {}:
        return pd.DataFrame(), pd.DataFrame()

    def transform_data_to_dataframe(data, completed: bool):
        rows = []
        for url, match_data in data.items():
            summary = match_data['match_summary']
            if summary["tournament_info"]["tournament_name"] != "OLYMPIC GAMES":

                if not completed:
                    summary['player1']['is_winner'] = True
                if summary['player1']['is_winner']:
                    winner, loser = summary['player1'], summary['player2']
                else:
                    winner, loser = summary['player2'], summary['player1']

                row = {"url": url, "tournament_name": summary["tournament_info"]["tournament_name"],
                       "tournament_location": summary["tournament_info"]["tournament_name"],
                       "tournament_country": summary["tournament_info"]["location"],
                       "surface": summary["tournament_info"]["surface"],
                       "indoor_or_outdoor": summary["tournament_info"]["court"],
                       "round_name": summary["tournament_info"]["round_name"], "date": summary["time_and_date"]["date"],
                       "time": summary["time_and_date"]["time"], "winner_name": winner["name"],
                       "winner_rank": winner["rank"], "winner_seed": winner.get("seed", ""),
                       "loser_name": loser["name"], "loser_rank": loser["rank"], "loser_seed": loser.get("seed", ""),
                       "AvgL": loser["odds"], "AvgW": winner["odds"], "scheduled": True}

                if completed:
                    row["scheduled"] = False
                    row["comment"] = summary["comment"]
                    if summary["comment"] == "WALKOVER" or summary["tournament_info"][
                        "tournament_name"] == "OLYMPIC GAMES":
                        row.update({
                            "winner_sets": "",
                            "loser_sets": "",
                            "duration": ""
                        })
                    else:
                        row.update({
                            "winner_sets": summary["sets_score"]["Wsets"],
                            "loser_sets": summary["sets_score"]["Lsets"],
                            "duration": summary["duration"]
                        })

                        winner_scores = summary["scores_by_set"].get(
                            "player1" if summary['player1']['is_winner'] else "player2", {})
                        loser_scores = summary["scores_by_set"].get(
                            "player2" if summary['player1']['is_winner'] else "player1",
                            {})

                        for set in range(1, 6):
                            row[f"winner_Set {set}"] = np.nan
                        for set in range(1, 6):
                            row[f"loser_Set {set}"] = np.nan

                        for set_num, score in winner_scores.items():
                            row[f"winner_{set_num}"] = score
                        for set_num, score in loser_scores.items():
                            row[f"loser_{set_num}"] = score

                        stats = match_data.get('match_statistics', {})

                        if summary['player1']['is_winner']:
                            for stat_name, values in stats.items():
                                row[f"winner_{stat_name}"] = values[0]
                                row[f"loser_{stat_name}"] = values[1]
                        else:
                            for stat_name, values in stats.items():
                                row[f"winner_{stat_name}"] = values[1]
                                row[f"loser_{stat_name}"] = values[0]

                rows.append(row)

        return pd.DataFrame(rows)

    df = transform_data_to_dataframe(livesport, completed)

    df['tournament_location'] = df['tournament_location'].str.lower()

    mapping = {
        'hertogenbosch': "'s-hertogenbosch",
        'paris': 'paris 2',
        'london': 'queens club',
        'australian open': 'melbourne',
        'french open': 'paris',
        'wimbledon': 'london',
        'us open': 'new york',
    }
    df['tournament_location'] = df['tournament_location'].replace(mapping)

    df['winner_name'] = df['winner_name'].str.lower()
    df['loser_name'] = df['loser_name'].str.lower()

    with open(f"raw_data/tennis_explorer/player_details_with_id.json") as f:
        player_details = json.load(f)

    def manual_name_normalization(full_name):
        if full_name == "McCabe James":
            return "Mccabe J."
        if full_name == "Rehberg Max Hans":
            return "Rehberg M."
        if full_name == "Bailly Gilles Arnaud":
            return "Bailly G."
        if full_name == "Barrios Vera Marcelo Tomas":
            return "Barrios Vera T."
        if full_name == "O'Connell Christopher":
            return "O Connell C."
        if full_name == "Etcheverry Tomas Martin":
            return 'Etcheverry T.'
        if full_name == "Zhang Zhizhen":
            return 'Zhang Zh.'
        if full_name == "Burruchaga Roman Andres":
            return "Burruchaga R."
        if full_name == "Meligeni Rodrigues Alves Felipe":
            return "Meligeni Alves F."
        if full_name == "Damm Martin (2003)":
            return "Damm M."
        if full_name == "Mpetshi Perricard Giovanni":
            return "Mpetshi G."
        if full_name == "McDonald Mackenzie":
            return "Mcdonald M."
        if full_name == "Hong Seong Chan":
            return "Hong S."
        if full_name == "Gomez Federico Agustin":
            return "Gomez F."
        return None

    def generate_random_player_info(df_name, existing_ids):
        new_id = str(random.randint(100000, 999999))
        while new_id in existing_ids:
            new_id = str(random.randint(100000, 999999))
        existing_ids.append(new_id)
        return {
            "Name": df_name,
            "Country": "Switzerland",
            "Height": "185 cm",
            "Date_of_birth": "1998-06-24",
            "Plays": "right",
            "normalized_name": df_name,
            "id": new_id,
        }

    def normalize_name(json_name, df_names):
        json_name = json_name.lower()
        manual_case = manual_name_normalization(json_name)
        if manual_case:
            return manual_case
        json_parts = re.split(r'[ -]', json_name)
        json_parts = [part for part in json_parts if part]
        for df_name in df_names:
            df_name = df_name.lower()
            df_parts = re.split(r'[ .-]', df_name)
            df_parts = [part for part in df_parts if part]
            exact_match = any(part in json_parts for part in df_parts)
            if not exact_match:
                continue

            matched_parts = set()
            for df_part in df_parts:
                match_found = False
                for json_part in json_parts:
                    if json_part in matched_parts:
                        continue

                    if df_part == json_part or df_part == json_part[0]:
                        matched_parts.add(json_part)
                        match_found = True
                        break

                if not match_found:
                    break

            if len(matched_parts) == len(df_parts):
                return df_name

        return 'unset'

    for player in player_details:
        player["normalized_name"] = 'unset'

    for player in player_details:
        if player["normalized_name"] == 'unset':
            player["normalized_name"] = normalize_name(player["Name"], df['winner_name'].unique())
    for player in player_details:
        if player["normalized_name"] == 'unset':
            player["normalized_name"] = normalize_name(player["Name"], df['loser_name'].unique())

    details_lookup = {player['normalized_name']: player for player in player_details}
    existing_ids = [player["id"] for player in player_details]
    for index, row in df.iterrows():
        winner_name = row['winner_name']
        if winner_name in details_lookup:
            winner_details = details_lookup[winner_name]
        else:
            winner_details = generate_random_player_info(winner_name, existing_ids)
            player_details.append(winner_details)
            print(f"Generated random player info for player: {winner_name}")
        for key, value in winner_details.items():
            if key != 'normalized_name':
                col_name = f"winner_{key}"
                if col_name not in df.columns:
                    df[col_name] = None
                df.at[index, col_name] = value

        loser_name = row['loser_name']
        if loser_name in details_lookup:
            loser_details = details_lookup[loser_name]
        else:
            loser_details = generate_random_player_info(loser_name, existing_ids)
            player_details.append(loser_details)
            print(f"Generated random player info for player: {loser_name}")
        for key, value in loser_details.items():
            if key != 'normalized_name':
                col_name = f"loser_{key}"
                if col_name not in df.columns:
                    df[col_name] = None
                df.at[index, col_name] = value

    with open(f"raw_data/tennis_explorer/player_details_with_id.json", "w") as file:
        json.dump(player_details, file, indent=4)

    df['winner_Date_of_birth'] = df['winner_Date_of_birth'].fillna("1998-06-24")
    df['loser_Date_of_birth'] = df['loser_Date_of_birth'].fillna("1998-06-24")
    df['winner_Country'] = df['winner_Country'].fillna("Switzerland")
    df['loser_Country'] = df['loser_Country'].fillna("Switzerland")
    df['winner_Plays'] = df['winner_Plays'].fillna("Right")
    df['loser_Plays'] = df['loser_Plays'].fillna("Right")
    df['winner_Height'] = df['winner_Height'].fillna("185 cm")
    df['loser_Height'] = df['loser_Height'].fillna("185 cm")

    rename_mapping = {
        'location': 'tournament_location',
        'surface': 'Surface',
        'comment': 'Comment',
        'round_name': 'Round',
        'date': 'Date',
        'time': 'time',
        'winner_name': 'winner_name',
        'loser_name': 'loser_name',
        'winner_Set 1': 'W1',
        'loser_Set 1': 'L1',
        'winner_Set 2': 'W2',
        'loser_Set 2': 'L2',
        'winner_Set 3': 'W3',
        'loser_Set 3': 'L3',
        'winner_Set 4': 'W4',
        'loser_Set 4': 'L4',
        'winner_Set 5': 'W5',
        'loser_Set 5': 'L5',
        'winner_sets': 'Wsets',
        'loser_sets': 'Lsets',
        'duration': 'minutes',
        'winner_Aces': 'w_ace',
        'loser_Aces': 'l_ace',
        'winner_Double Faults': 'w_df',
        'loser_Double Faults': 'l_df',
        'winner_rank': 'winner_rank',
        'loser_rank': 'loser_rank',
        'winner_Country': 'winner_ioc',
        'loser_Country': 'loser_ioc',
        'winner_Plays': 'winner_hand',
        'loser_Plays': 'loser_hand'
    }

    df.rename(columns=rename_mapping, inplace=True)

    def process_seed(value):
        if value.isdigit() or value == '':
            return value, ''
        elif value == 'Q/LL':
            return '', 'Q'
        else:
            return '', value

    df['winner_seed'], df['winner_entry'] = zip(*df['winner_seed'].apply(process_seed))
    df['loser_seed'], df['loser_entry'] = zip(*df['loser_seed'].apply(process_seed))

    def calculate_age(dob):
        if pd.isna(dob):
            return None
        dob = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    df['winner_age'] = df['winner_Date_of_birth'].apply(calculate_age)
    df['loser_age'] = df['loser_Date_of_birth'].apply(calculate_age)

    with open("raw_data/reddit/tournaments.json", 'r') as file:
        tournaments_2025 = json.load(file)

    df['tournament_level'] = df['tournament_location'].map(tournaments_2025)

    df['winner_id'] = df['winner_id'].astype(str)
    df['loser_id'] = df['loser_id'].astype(str)

    # Normalize player IDs so the smaller lexicographical ID is always first
    df['player1_id'] = df[['winner_id', 'loser_id']].min(axis=1).astype(str)
    df['player2_id'] = df[['winner_id', 'loser_id']].max(axis=1).astype(str)

    df['match_id'] = df['tournament_location'].astype(str) + '_' + '2025' + '_' + df['player1_id'] + '_' + df[
        'player2_id']

    rename_mapping = {
        "SLAM": "Grand Slam",
        "MASTERS 1000": 'Masters 1000',
    }
    df['tournament_level'] = df['tournament_level'].replace(rename_mapping)
    df['best_of'] = df['tournament_level'].apply(lambda x: 5 if x == 'Grand Slam' else 3)
    raw_df = df.copy()
    if completed:
        columns_to_modify = ['W1', 'W2', 'W3', 'W4', 'W5', 'L1', 'L2', 'L3', 'L4', 'L5']

        df[columns_to_modify] = df[columns_to_modify].map(
            lambda x: str(x).strip()[0] if pd.notna(x) and str(x).strip() else x)
        raw_df = df.copy()

        df[['w_1stWon', 'w_1stIn']] = df['winner_1st Serve Points Won'].str.extract(r'\((\d+)/(\d+)\)')
        df.drop(columns=['winner_1st Serve Points Won'], inplace=True)

        df[['l_1stWon', 'l_1stIn']] = df['loser_1st Serve Points Won'].str.extract(r'\((\d+)/(\d+)\)')
        df.drop(columns=['loser_1st Serve Points Won'], inplace=True)

        df[['to_drop', 'w_SvGms']] = df['winner_Service Games Won'].str.extract(r'\((\d+)/(\d+)\)')
        df.drop(columns=['winner_Service Games Won'], inplace=True)

        df[['to_drop', 'l_SvGms']] = df['loser_Service Games Won'].str.extract(r'\((\d+)/(\d+)\)')
        df.drop(columns=['loser_Service Games Won'], inplace=True)

        df[['w_2ndWon', 'to_drop']] = df['winner_2nd Serve Points Won'].str.extract(r'\((\d+)/(\d+)\)')
        df.drop(columns=['winner_2nd Serve Points Won'], inplace=True)

        df[['l_2ndWon', 'to_drop']] = df['loser_2nd Serve Points Won'].str.extract(r'\((\d+)/(\d+)\)')
        df.drop(columns=['loser_2nd Serve Points Won'], inplace=True)

        df[['w_bpSaved', 'w_bpFaced']] = df['winner_Break Points Saved'].str.extract(r'\((\d+)/(\d+)\)')
        df.drop(columns=['winner_Break Points Saved'], inplace=True)

        df[['l_bpSaved', 'l_bpFaced']] = df['loser_Break Points Saved'].str.extract(r'\((\d+)/(\d+)\)')
        df.drop(columns=['loser_Break Points Saved'], inplace=True)

        df[['to_drop', 'w_svpt']] = df['winner_Service Points Won'].str.extract(r'\((\d+)/(\d+)\)')
        df.drop(columns=['winner_Service Points Won'], inplace=True)

        df[['to_drop', 'l_svpt']] = df['loser_Service Points Won'].str.extract(r'\((\d+)/(\d+)\)')
        df.drop(columns=['loser_Service Points Won'], inplace=True)

        df['Comment'] = df['Comment'].apply(lambda x: 'RETIRED' if 'RETIRED' in x else x)

        df['Comment'] = df['Comment'].str.lower()

        columns_to_update = ['W1', 'W2', 'W3', 'W4', 'W5', 'L1', 'L2', 'L3', 'L4', 'L5', 'Wsets', 'Lsets', 'minutes']
        df[columns_to_update] = df[columns_to_update].replace('', np.nan)
        df.loc[df['Comment'].isin(['disqualified', 'retired', 'walkover', 'awarded']), columns_to_update] = df.loc[
            df['Comment'].isin(['disqualified', 'retired', 'walkover', 'awarded']), columns_to_update].fillna(0)

        average_minutes = df[df['Comment'] == 'completed'].groupby('best_of')['minutes'].mean().round()
        df.loc[(df['Comment'] == 'completed') & (df['minutes'].isnull()), 'minutes'] = df['best_of'].map(
            average_minutes)

        df['minutes'] = df['minutes'].apply(
            lambda x: x if x == 0 else int(x.split(':')[0]) * 60 + int(x.split(':')[1])
        )

    df.drop(columns=['winner_Winners', 'loser_Winners', 'winner_Unforced Errors', 'loser_Unforced Errors',
                     'winner_Net Points Won', 'loser_Net Points Won', 'winner_Return Points Won',
                     'loser_Return Points Won', 'winner_Total Points Won', 'loser_Total Points Won',
                     'winner_Last 10 Balls',
                     'loser_Last 10 Balls', 'winner_Match Points Saved', 'loser_Match Points Saved',
                     'winner_Return Games Won', 'loser_Return Games Won', 'winner_Total Games Won',
                     'loser_Total Games Won',
                     'winner_1st Serve Percentage', 'loser_1st Serve Percentage', 'winner_1st Return Points Won',
                     'loser_1st Return Points Won', 'winner_2nd Return Points Won', 'loser_2nd Return Points Won',
                     'winner_Break Points Converted',
                     'loser_Break Points Converted', 'winner_Distance Covered (metres)',
                     'loser_Distance Covered (metres)',
                     'winner_Average 1st Serve Speed', 'loser_Average 1st Serve Speed',
                     'winner_Average 2nd Serve Speed',
                     'loser_Average 2nd Serve Speed', 'to_drop', 'winner_Height', 'loser_Height'], errors='ignore',
            inplace=True)

    values_to_encode = ['WC', 'Q', 'LL']

    df['winner_entry'] = df['winner_entry'].where(df['winner_entry'].isin(values_to_encode))
    df['loser_entry'] = df['loser_entry'].where(df['loser_entry'].isin(values_to_encode))

    entries = ['LL', 'Q', 'WC']
    df = pd.get_dummies(df, columns=['winner_entry'], prefix='winner_entry', prefix_sep='_')
    df = pd.get_dummies(df, columns=['loser_entry'], prefix='loser_entry', prefix_sep='_')
    for entry in entries:
        column_name = f"winner_entry_{entry}"
        if column_name not in df.columns:
            df[column_name] = 0
        column_name = f"loser_entry_{entry}"
        if column_name not in df.columns:
            df[column_name] = 0

    df['winner_seed'] = df['winner_seed'].replace('', np.nan)
    df['loser_seed'] = df['loser_seed'].replace('', np.nan)

    df['winner_is_seeded'] = df['winner_seed'].notna().astype(int)
    df['loser_is_seeded'] = df['loser_seed'].notna().astype(int)
    df = df.drop(columns=['winner_seed', 'loser_seed'])

    df['winner_rank'] = df['winner_rank'].replace('', np.nan)
    df['loser_rank'] = df['loser_rank'].replace('', np.nan)

    df.loc[df['winner_rank'].isnull(), 'winner_rank'] = 2000
    df.loc[df['loser_rank'].isnull(), 'loser_rank'] = 2000

    df['tournament_id'] = df['tournament_location'].astype(str) + '_2025'

    column_type_mapping = {
        "tournament_location": "object",
        "tournament_name": "object",
        "Date": "object",
        "indoor_or_outdoor": "object",
        "Surface": "object",
        "Round": "object",
        "W1": "float64",
        "L1": "float64",
        "W2": "float64",
        "L2": "float64",
        "W3": "float64",
        "L3": "float64",
        "W4": "float64",
        "L4": "float64",
        "W5": "float64",
        "L5": "float64",
        "Wsets": "float64",
        "Lsets": "float64",
        "Comment": "object",
        "AvgW": "float64",
        "AvgL": "float64",
        "loser_id": "int64",
        "winner_id": "int64",
        "match_id": "object",
        "tournament_id": "object",
        "draw_size": "int64",
        "tournament_level": "object",
        "tournament_date": "object",
        "winner_name": "object",
        "winner_hand": "object",
        "winner_ht": "float64",
        "winner_ioc": "object",
        "winner_age": "float64",
        "loser_name": "object",
        "loser_hand": "object",
        "loser_ht": "float64",
        "loser_ioc": "object",
        "loser_age": "float64",
        "best_of": "int64",
        "minutes": "float64",
        "w_ace": "float64",
        "w_df": "float64",
        "w_svpt": "float64",
        "w_1stIn": "float64",
        "w_1stWon": "float64",
        "w_2ndWon": "float64",
        "w_SvGms": "float64",
        "w_bpSaved": "float64",
        "w_bpFaced": "float64",
        "l_ace": "float64",
        "l_df": "float64",
        "l_svpt": "float64",
        "l_1stIn": "float64",
        "l_1stWon": "float64",
        "l_2ndWon": "float64",
        "l_SvGms": "float64",
        "l_bpSaved": "float64",
        "l_bpFaced": "float64",
        "winner_rank": "float64",
        "winner_rank_points": "float64",
        "loser_rank": "float64",
        "loser_rank_points": "float64",
        "time": "object",
        "winner_entry_LL": "bool",
        "winner_entry_Q": "bool",
        "winner_entry_WC": "bool",
        "loser_entry_LL": "bool",
        "loser_entry_Q": "bool",
        "loser_entry_WC": "bool",
        "winner_is_seeded": "int64",
        "loser_is_seeded": "int64",
    }
    for col, dtype in column_type_mapping.items():
        if col in df.columns:
            try:
                df[col] = df[col].astype(dtype)
            except (ValueError, TypeError):
                print(f"Could not convert column {col} to {dtype}")

    df['Date'] = pd.to_datetime(df['Date'])

    round_mapping = {
        '1/64-FINALS': '1st Round',
        '1/32-FINALS': '2nd Round',
        '1/16-FINALS': '3rd Round',
        '1/8-FINALS': '4th Round',
        'QUARTER-FINALS': 'Quarterfinals',
        'SEMI-FINALS': 'Semifinals',
        'FINAL': 'The Final'
    }
    df['Round'] = df['Round'].replace(round_mapping)
    missing_values = df.isnull().sum()

    columns_with_nan = missing_values[missing_values > 0]

    print("Columns with NaN values and their counts:")
    print(columns_with_nan)
    df = df.sort_values(by='Date', ascending=True)
    return raw_df, df
