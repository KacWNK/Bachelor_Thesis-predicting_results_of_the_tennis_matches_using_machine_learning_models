import pandas as pd
from feature_creation.src.python import (add_fatigue_scores, add_elo_rating, add_h2h, add_aggregated_player_stats,
                                         add_home_advantage,
                                         add_injury, add_current_tournament_stats, add_tournament_win_loss_history,
                                         add_last_10_win_record,
                                         prepare_before_model, generate_predictions_neural_net)

FEATURE_FUNCTIONS = [
    add_elo_rating,
    add_last_10_win_record,
    add_fatigue_scores, add_aggregated_player_stats,
    add_h2h, add_home_advantage, add_injury, add_current_tournament_stats, add_tournament_win_loss_history
]


class IterativeDataFrameProcessor:
    def __init__(self, initial_df, feature_functions):
        self.df = initial_df
        self.feature_functions = feature_functions

    def calculate_new_columns(self, new_rows):
        new_rows = new_rows.copy()

        for func in self.feature_functions:
            print(f"Adding columns using {func.__name__}")
            new_rows = func(new_rows, self.df)

        return new_rows

    def add_rows(self, new_rows):
        processed_rows = self.calculate_new_columns(new_rows)
        existing_ids = self.df['match_id']
        rows_to_update = processed_rows[processed_rows['match_id'].isin(existing_ids)]

        self.df.set_index('match_id', inplace=True)
        rows_to_update.set_index('match_id', inplace=True)
        self.df.update(rows_to_update)
        self.df.reset_index(inplace=True)

        rows_to_append = processed_rows[~processed_rows['match_id'].isin(existing_ids)]

        self.df = pd.concat([self.df, rows_to_append], ignore_index=True)
        return processed_rows

    def get_dataframe(self):
        return self.df


def process_new_data(new_matches, existing_matches):
    new_matches['Date'] = pd.to_datetime(new_matches['Date'])

    processor = IterativeDataFrameProcessor(existing_matches, feature_functions=FEATURE_FUNCTIONS)

    new_matches_processed = processor.add_rows(new_matches)
    updated_df = processor.get_dataframe()

    new_matches_prepared = prepare_before_model(new_matches_processed)
    predictions_neural_net = generate_predictions_neural_net(new_matches_prepared)
    return updated_df, new_matches_processed, predictions_neural_net
