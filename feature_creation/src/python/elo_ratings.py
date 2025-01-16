import pandas as pd
from collections import defaultdict
from datetime import datetime, timedelta


def create_player_ranks(matches_df):
    player_ranks = {}

    for index, row in matches_df.iterrows():
        winner_id = row['winner_id']
        loser_id = row['loser_id']
        winner_rank = row['winner_rank']
        loser_rank = row['loser_rank']

        # Add the winner's rank if not already in the dictionary
        if winner_id not in player_ranks:
            player_ranks[winner_id] = winner_rank

        # Add the loser's rank if not already in the dictionary
        if loser_id not in player_ranks:
            player_ranks[loser_id] = loser_rank

    return player_ranks


class EloRatingsProcessor:
    def __init__(self, matches_df, new_matches_df, player_ranks):
        self.matches_df = matches_df
        self.new_matches_df = new_matches_df
        self.player_ranks = player_ranks
        self.current_ratings = self.initialize_ratings()
        self.momentum = defaultdict(lambda: 1.0)

    def initialize_ratings(self):
        players = set(self.matches_df['winner_id']).union(set(self.matches_df['loser_id']))
        surface_ratings = {}

        for player in players:
            atp_rank = self.player_ranks.get(player, 1000)

            # Initialize rating based on ATP rank
            if atp_rank <= 10:
                initial_rating = 2000
            elif atp_rank <= 50:
                initial_rating = 1900
            elif atp_rank <= 100:
                initial_rating = 1800
            elif atp_rank <= 500:
                initial_rating = 1600
            else:
                initial_rating = 1500

            # # Adjust surface-specific initial ratings based on surface win rates
            surface_ratings[player] = {
                'General': initial_rating,
                'Hard': initial_rating,
                'Clay': initial_rating,
                'Grass': initial_rating
            }

        return surface_ratings

    def blended_rating(self, overall_rating, surface_rating, num_surface_matches, base_weight=0.2):
        # Increase weight of surface rating if the player has many matches on that surface
        weight = base_weight if num_surface_matches < 10 else 0.4
        return (weight * surface_rating) + ((1 - weight) * overall_rating)

    def dynamic_k_factor(self, matches_by_date, player_id):
        # Calculate base K-factor based on matches count
        total_matches = len(matches_by_date[player_id])
        base_k = 210 / ((total_matches + 5) ** 0.5)

        # Apply momentum factor to K
        k = base_k * self.momentum[player_id]
        return k

    @staticmethod
    def update_matches_history(matches_history, player_id, surface, current_date):
        # Track match count within the past year
        if isinstance(current_date, str):
            current_date = datetime.strptime(current_date, "%Y-%m-%d")

        one_year_ago = current_date - timedelta(days=365)

        # Remove outdated matches
        matches_history[surface][player_id] = [date for date in matches_history[surface][player_id] if
                                               date > one_year_ago]

        # Add current match
        matches_history[surface][player_id].append(current_date)

    def update_momentum(self, winner_id, loser_id):
        # Increase momentum for winner, up to a max (e.g., 1.5)
        self.momentum[winner_id] = min(self.momentum[winner_id] + 0.06, 1.3)

        # Decrease momentum for loser, down to a minimum (e.g., 0.7)
        self.momentum[loser_id] = max(self.momentum[loser_id] - 0.06, 0.7)

        # Slightly decay momentum for all players after each match
        for player in self.momentum:
            if player != winner_id and player != loser_id:
                self.momentum[player] = 1.0 + (self.momentum[player] - 1.0) * 0.99  # Decay toward 1.0

    def win_probability(self, rating_a, rating_b):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def update_ratings(self, tourney_level, matches_history, winner_id, loser_id, surface, current_date):
        general_rating_winner = self.current_ratings[winner_id]['General']
        general_rating_loser = self.current_ratings[loser_id]['General']
        surface_rating_winner = self.current_ratings[winner_id][surface]
        surface_rating_loser = self.current_ratings[loser_id][surface]

        general_winner_probability = self.win_probability(general_rating_winner, general_rating_loser)
        general_loser_probability = 1 - general_winner_probability
        surface_winner_probability = self.win_probability(surface_rating_winner, surface_rating_loser)
        surface_loser_probability = 1 - surface_winner_probability

        # Update match counts
        self.update_matches_history(matches_history, winner_id, 'General', current_date)
        self.update_matches_history(matches_history, loser_id, 'General', current_date)
        self.update_matches_history(matches_history, winner_id, surface, current_date)
        self.update_matches_history(matches_history, loser_id, surface, current_date)

        # Tournament level K-factor adjustment
        k_level = 1.2 if tourney_level == "Grand Slam" else (
            1.05 if tourney_level == "Masters" else (1.0 if tourney_level == "ATP 500" else 0.9))

        # Calculate K-factors with momentum applied
        k_general_winner = self.dynamic_k_factor(matches_history['General'], winner_id) * k_level
        k_general_loser = self.dynamic_k_factor(matches_history['General'], loser_id) * k_level
        k_surface_winner = self.dynamic_k_factor(matches_history[surface], winner_id) * k_level
        k_surface_loser = self.dynamic_k_factor(matches_history[surface], loser_id) * k_level

        # Update general and surface ratings
        self.current_ratings[winner_id]['General'] += k_general_winner * (1 - general_winner_probability)
        self.current_ratings[loser_id]['General'] += k_general_loser * (0 - general_loser_probability)
        self.current_ratings[winner_id][surface] += k_surface_winner * (1 - surface_winner_probability)
        self.current_ratings[loser_id][surface] += k_surface_loser * (0 - surface_loser_probability)

        # Update momentum based on the match outcome
        self.update_momentum(winner_id, loser_id)

        return general_rating_winner, general_rating_loser, surface_rating_winner, surface_rating_loser

    # Step 5: Process Matches and Calculate Brier Score
    def insert_elo_ratings_to_df(self):
        matches_history = {
            'General': defaultdict(lambda: defaultdict(list)),
            'Hard': defaultdict(lambda: defaultdict(list)),
            'Clay': defaultdict(lambda: defaultdict(list)),
            'Grass': defaultdict(lambda: defaultdict(list))
        }
        elo_winners, elo_losers = [], []
        surface_elo_winners, surface_elo_losers = [], []
        blended_elo_winners, blended_elo_losers = [], []

        for index, row in self.matches_df.iterrows():
            winner_id, loser_id, surface, current_date = row['winner_id'], row['loser_id'], row['Surface'], row['Date']
            general_rating_winner, general_rating_loser, surface_rating_winner, surface_rating_loser = self.update_ratings(
                row['tournament_level'], matches_history, winner_id, loser_id, surface, current_date)

            num_surface_matches_winner = len(matches_history[surface][winner_id])
            num_surface_matches_loser = len(matches_history[surface][loser_id])

            if index >= len(self.matches_df) - len(self.new_matches_df):
                elo_winners.append(general_rating_winner)
                elo_losers.append(general_rating_loser)
                surface_elo_winners.append(surface_rating_winner)
                surface_elo_losers.append(surface_rating_loser)
                blended_elo_winners.append(
                    self.blended_rating(general_rating_winner, surface_rating_winner, num_surface_matches_winner))
                blended_elo_losers.append(
                    self.blended_rating(general_rating_loser, surface_rating_loser, num_surface_matches_loser))

        self.new_matches_df['elo_winner'] = elo_winners
        self.new_matches_df['elo_loser'] = elo_losers
        self.new_matches_df['surface_elo_winner'] = surface_elo_winners
        self.new_matches_df['surface_elo_loser'] = surface_elo_losers
        self.new_matches_df['blended_elo_winner'] = blended_elo_winners
        self.new_matches_df['blended_elo_loser'] = blended_elo_losers


def add_elo_rating(new_rows: pd.DataFrame, existing_df: pd.DataFrame) -> pd.DataFrame:
    combined_df = pd.concat([existing_df, new_rows], ignore_index=True) if existing_df is not None else new_rows
    combined_df = combined_df.drop_duplicates().reset_index(drop=True)
    player_ranks = create_player_ranks(combined_df)

    complex_elo_ratings_predictor = EloRatingsProcessor(combined_df, new_rows, player_ranks)
    complex_elo_ratings_predictor.insert_elo_ratings_to_df()
    return new_rows
