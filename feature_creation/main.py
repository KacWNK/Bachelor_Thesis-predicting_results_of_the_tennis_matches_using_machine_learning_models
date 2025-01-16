import pandas as pd
from src.python import (add_fatigue_scores, add_elo_rating, add_h2h, add_aggregated_player_stats, add_home_advantage,
                        add_injury, add_current_tournament_stats, add_tournament_win_loss_history)

FEATURE_FUNCTIONS = [
    add_fatigue_scores,
    add_elo_rating, add_aggregated_player_stats,
    add_h2h, add_home_advantage, add_injury, add_current_tournament_stats, add_tournament_win_loss_history
]


class IterativeDataFrameProcessor:
    def __init__(self, initial_df, feature_functions):
        self.df = initial_df
        self.feature_functions = feature_functions

    def calculate_new_columns(self, new_rows):
        new_rows = new_rows.copy()

        # Iteruj przez wiersze i zastosuj każdą funkcję z listy
        for func in self.feature_functions:
            new_rows = func(new_rows, self.df)

        return new_rows

    def add_rows(self, new_rows):
        processed_rows = self.calculate_new_columns(new_rows)

        # Dodaj przetworzone wiersze do istniejącej ramki
        self.df = pd.concat([self.df, processed_rows], ignore_index=True)

    def get_dataframe(self):
        return self.df


if __name__ == "__main__":
    # Wczytaj dane wejściowe
    input_path = "data/input_matches.csv"
    output_path = "data/processed_matches.csv"

    existing_matches = pd.read_csv(output_path)
    new_matches = pd.read_csv(input_path)
    new_matches['Date'] = pd.to_datetime(new_matches['Date'], errors='coerce')
    new_matches = new_matches[new_matches["Date"].dt.year == 2019]

    processor = IterativeDataFrameProcessor(existing_matches, feature_functions=FEATURE_FUNCTIONS)

    processor.add_rows(new_matches)
    updated_df = processor.get_dataframe()

    # Zapisz wyniki
    updated_df.to_csv(output_path, index=False)
    print(f"Dane z cechami zapisane do {output_path}")
