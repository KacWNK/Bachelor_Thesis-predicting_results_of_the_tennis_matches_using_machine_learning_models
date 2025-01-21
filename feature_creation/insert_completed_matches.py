import pandas as pd
from typing import Union


def insert_completed_matches_to_matches_df(completed_matches: Union[list[dict], pd.DataFrame],
                                           existing_matches: pd.DataFrame, match_id_field="match_id") -> pd.DataFrame:
    if isinstance(completed_matches, list):
        completed_matches = pd.DataFrame(completed_matches)

    for _, row in completed_matches.iterrows():
        match_id = row[match_id_field]

        if match_id in existing_matches[match_id_field].values:
            idx = existing_matches.index[existing_matches[match_id_field] == match_id].tolist()[0]

            for col in row.index:
                if col != match_id_field:
                    existing_matches.at[idx, col] = row[col]

    return existing_matches


input_path = "../data/completed_matches.csv"
completed_matches = pd.read_csv(input_path)

matches_df = pd.read_csv("data/matches_2018-2024.csv")

# Update the DataFrame
updated_df = insert_completed_matches_to_matches_df(completed_matches, matches_df)

# Output the result
updated_df.to_csv("data/processed_matches.csv")
