import pandas as pd


def validate_condition(condition: bool, success_message: str, error_message: str, raise_error: bool = True) -> None:
    if condition:
        print(success_message)
    else:
        if raise_error:
            raise ValueError(error_message)
        else:
            print(error_message)


def check_columns_same(dataframes: dict[str, pd.DataFrame], raise_error: bool = True) -> None:
    years = list(dataframes.keys())
    first_columns = set(dataframes[years[0]].columns)

    for year in years[1:]:
        current_columns = set(dataframes[year].columns)
        condition = current_columns == first_columns

        success_message = f"✅ Year {year}: Columns match with the first year ({years[0]})."
        error_message = f"❌ Year {year}: Columns differ from the first year ({years[0]})."

        validate_condition(condition, success_message, error_message, raise_error)


def compare_tourney_locations(
        yearly_data_1: dict[str, pd.DataFrame],
        yearly_data_2: dict[str, pd.DataFrame],
        name1: str = "Dataset 1",
        name2: str = "Dataset 2",
        raise_error: bool = True,
) -> None:
    for year in yearly_data_1:
        if year not in yearly_data_2:
            raise KeyError(f"Year {year} exists in {name1} but not in {name2}. Check the datasets.")

        unique_to_data1 = (
            yearly_data_1[year][~yearly_data_1[year]['tourney_location'].isin(yearly_data_2[year]['tourney_location'])]
            ['tourney_location']
            .unique()
        )
        unique_to_data2 = (
            yearly_data_2[year][~yearly_data_2[year]['tourney_location'].isin(yearly_data_1[year]['tourney_location'])]
            ['tourney_location']
            .unique()
        )

        condition = unique_to_data1.size == 0 and unique_to_data2.size == 0
        error_message = f"""
            ❌ Mismatch in 'tourney_location' for year {year}:
            - Unique to {name1}: {unique_to_data1.tolist()}
            - Unique to {name2}: {unique_to_data2.tolist()}
            """
        success_message = f"✅ 'tourney_location' column matches for year {year}."
        validate_condition(condition, success_message, error_message, raise_error)


def check_one_to_one_mapping(
        yearly_data: dict[str, pd.DataFrame], column_pairs: list[tuple[str, str]], raise_error: bool = True
) -> None:
    for year, df in yearly_data.items():
        for col1, col2 in column_pairs:
            unique_col1 = df[col1].nunique()
            unique_col2 = df[col2].nunique()

            condition = unique_col1 == unique_col2
            error_message = f"""
            ❌ One-to-one mapping violation between '{col1}' and '{col2}' in year {year}:
            - Unique '{col1}': {unique_col1}
            - Unique '{col2}': {unique_col2}
            This suggests that some '{col1}' values map to multiple '{col2}' values or vice versa.
            """
            success_message = f"✅ Year {year}: One-to-one mapping between '{col1}' and '{col2}' is valid."
            validate_condition(condition, success_message, error_message, raise_error)


def check_missing_player_ids(yearly_data: dict[str, pd.DataFrame], raise_error: bool = True) -> None:
    for year, df in yearly_data.items():
        missing_loser_ids = df[df['loser_id'].isna()]
        unique_losers = missing_loser_ids['Loser'].unique()

        missing_winner_ids = df[df['winner_id'].isna()]
        unique_winners = missing_winner_ids['Winner'].unique()

        error_message = ''
        if unique_losers.size > 0:
            error_message += f"❌ Missing 'loser_id' values:\n- Unique 'Loser' names: {unique_losers.tolist()}\n"

        if unique_winners.size > 0:
            error_message += f"❌ Missing 'winner_id' values:\n- Unique 'Winner' names: {unique_winners.tolist()}"

        success_message = f"✅ Year {year}: No missing 'loser_id' or 'winner_id' values found."
        condition = error_message == ''
        validate_condition(condition, success_message, error_message, raise_error)


def check_match_id_uniqueness(yearly_data: dict[str, pd.DataFrame], name: str = "Dataset",
                              raise_error: bool = True) -> None:
    for year in yearly_data:
        df = yearly_data[year]
        unique_match_ids = df['match_id'].nunique()
        total_df_rows = len(df)
        condition = unique_match_ids == total_df_rows
        error_message = f"""
                ❌ Year {year}: Duplicate 'match_id' values found in {name} dataset.
                - Total rows: {total_df_rows}
                - Unique 'match_id': {unique_match_ids}
                """
        success_message = f"✅ Year {year}: All 'match_id' values are unique in {name} dataset."
        validate_condition(condition, success_message, error_message, raise_error)


def check_match_id_consistency(
        yearly_data_1: dict[str, pd.DataFrame],
        yearly_data_2: dict[str, pd.DataFrame],
        name1: str = "Dataset 1",
        name2: str = "Dataset 2",
        raise_error: bool = True,
) -> None:
    for year in sorted(set(yearly_data_1.keys()).intersection(yearly_data_2.keys()), key=int):
        missing_in_data2 = yearly_data_1[year][~yearly_data_1[year]['match_id'].isin(yearly_data_2[year]['match_id'])][
            'match_id'].unique()
        missing_in_data1 = yearly_data_2[year][~yearly_data_2[year]['match_id'].isin(yearly_data_1[year]['match_id'])][
            'match_id'].unique()

        condition = len(missing_in_data2) == 0 and len(missing_in_data1) == 0
        success_message = f"✅ Year {year}: `match_id` values are consistent between {name1} and {name2}."
        error_message = f"""
            ❌ Year {year}: Mismatch in `match_id` values between {name1} and {name2}.
            - `match_id` values in {name1} but not in {name2}: {missing_in_data2.tolist()}
            - `match_id` values in {name2} but not in {name1}: {missing_in_data1.tolist()}
            """
        validate_condition(condition, success_message, error_message, raise_error)
