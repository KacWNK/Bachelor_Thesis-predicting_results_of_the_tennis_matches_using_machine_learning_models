import pandas as pd
from django.core.management.base import BaseCommand
from stats.models import Player, Match, Tournament
from django.db.utils import IntegrityError
import os


class Command(BaseCommand):
    help = "Load data from CSV files into the database"

    def handle(self, *args, **kwargs):
        data_dir = os.path.join(os.path.dirname(__file__), '../../data')
        # Load Players
        players_path = os.path.join(data_dir, 'players.csv')
        players_df = pd.read_csv(players_path)

        # Ensure proper data handling for missing values
        players_df['rank'] = players_df['rank'].fillna('Unranked')  # Fill missing rank with 'Unranked'
        players_df['age'] = players_df['age'].fillna('Unknown')  # Fill missing age with 'Unknown'
        players_df['hand'] = players_df['hand'].fillna('Unknown')

        players = []
        for _, row in players_df.iterrows():
            players.append(Player(
                player_id=row['player_id'],
                name=row['name'],
                rank=row['rank'],
                age=row['age'],
                hand=row['hand']
            ))
        Player.objects.bulk_create(players, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f"{len(players)} players successfully loaded!"))

        # Load Tournaments
        tournaments_path = os.path.join(data_dir, 'tournaments.csv')
        tournaments_df = pd.read_csv(tournaments_path)
        tournaments = []
        for _, row in tournaments_df.iterrows():
            tournaments.append(Tournament(
                tournament_id=row['tournament_id'],
                name=row['tournament_name'],
                location=row['tournament_location'],
                date=row['tournament_date'],
                level=row['tournament_level'],
                draw_size=row['draw_size'],
                surface=row['Surface'],
                indoor_or_outdoor=row['indoor_or_outdoor']
            ))
        Tournament.objects.bulk_create(tournaments, ignore_conflicts=True)  # Avoid duplicate errors
        self.stdout.write(self.style.SUCCESS(f"{len(tournaments)} tournaments successfully loaded!"))

        # Load Matches
        matches_path = os.path.join(data_dir, 'matches.csv')
        matches_df = pd.read_csv(matches_path)

        # Helper function to handle NaN values
        def clean_value(value):
            return None if pd.isna(value) else value

        # Convert date column and ensure proper handling of missing values
        matches_df['date'] = pd.to_datetime(matches_df['date'], errors='coerce')

        matches = []
        for index, row in matches_df.iterrows():
            try:
                # Fetch related models
                winner = Player.objects.get(player_id=row['winner_id'])
                loser = Player.objects.get(player_id=row['loser_id'])
                tournament = Tournament.objects.get(tournament_id=row['tournament_id'])

                # Create or update the match
                matches.append(Match(
                    match_id=row['match_id'],
                    date=clean_value(row['date']),
                    tournament=tournament,
                    winner=winner,
                    loser=loser,
                    round=clean_value(row['Round']),
                    indoor_or_outdoor=clean_value(row['indoor_or_outdoor']),
                    best_of=clean_value(row['best_of']),
                    minutes=clean_value(row['minutes']),
                    winner_seed=clean_value(row['winner_seed']),
                    loser_seed=clean_value(row['loser_seed']),
                    winner_entry=clean_value(row['winner_entry']),
                    loser_entry=clean_value(row['loser_entry']),
                    winner_rank=clean_value(row['winner_rank']),
                    loser_rank=clean_value(row['loser_rank']),
                    winner_rank_points=clean_value(row['winner_rank_points']),
                    loser_rank_points=clean_value(row['loser_rank_points']),
                    winner_age=clean_value(row['winner_age']),
                    loser_age=clean_value(row['loser_age']),
                    w1=clean_value(row['W1']),
                    l1=clean_value(row['L1']),
                    w2=clean_value(row['W2']),
                    l2=clean_value(row['L2']),
                    w3=clean_value(row['W3']),
                    l3=clean_value(row['L3']),
                    w4=clean_value(row['W4']),
                    l4=clean_value(row['L4']),
                    w5=clean_value(row['W5']),
                    l5=clean_value(row['L5']),
                    wsets=clean_value(row['Wsets']),
                    lsets=clean_value(row['Lsets']),
                    w_ace=clean_value(row['w_ace']),
                    l_ace=clean_value(row['l_ace']),
                    w_df=clean_value(row['w_df']),
                    l_df=clean_value(row['l_df']),
                    w_bpSaved=clean_value(row['w_bpSaved']),
                    l_bpSaved=clean_value(row['l_bpSaved']),
                    w_bpFaced=clean_value(row['w_bpFaced']),
                    l_bpFaced=clean_value(row['l_bpFaced']),

                    w_svpt=clean_value(row['w_svpt']),
                    w_1stIn=clean_value(row['w_1stIn']),
                    w_1stWon=clean_value(row['w_1stWon']),
                    w_2ndWon=clean_value(row['w_2ndWon']),
                    w_SvGms=clean_value(row['w_SvGms']),
                    l_SvGms=clean_value(row['l_SvGms']),

                    winner_1st_serve_in_pct=clean_value(row['winner_1st_serve_in_pct']),
                    winner_1st_serve_win_pct=clean_value(row['winner_1st_serve_win_pct']),
                    winner_2nd_serve_in_pct=clean_value(row['winner_2nd_serve_in_pct']),
                    winner_2nd_serve_win_pct=clean_value(row['winner_2nd_serve_win_pct']),
                    winner_service_games_won_pct=clean_value(row['winner_service_games_won_pct']),

                    loser_1st_serve_in_pct=clean_value(row['loser_1st_serve_in_pct']),
                    loser_1st_serve_win_pct=clean_value(row['loser_1st_serve_win_pct']),
                    loser_2nd_serve_in_pct=clean_value(row['loser_2nd_serve_in_pct']),
                    loser_2nd_serve_win_pct=clean_value(row['loser_2nd_serve_win_pct']),
                    loser_service_games_won_pct=clean_value(row['loser_service_games_won_pct']),

                    winner_1st_serve_return_win_pct=clean_value(row['winner_1st_serve_return_win_pct']),
                    winner_2nd_serve_return_win_pct=clean_value(row['winner_2nd_serve_return_win_pct']),
                    winner_return_games_win_pct=clean_value(row['winner_return_games_win_pct']),

                    loser_1st_serve_return_win_pct=clean_value(row['loser_1st_serve_return_win_pct']),
                    loser_2nd_serve_return_win_pct=clean_value(row['loser_2nd_serve_return_win_pct']),
                    loser_return_games_win_pct=clean_value(row['loser_return_games_win_pct']),

                    winner_bp_won_pct=clean_value(row['winner_bp_won_pct']),
                    loser_bp_won_pct=clean_value(row['loser_bp_won_pct']),
                    winner_bp_saved_pct=clean_value(row['winner_bp_saved_pct']),
                    loser_bp_saved_pct=clean_value(row['loser_bp_saved_pct']),


                    comment=clean_value(row['Comment']),
                    avgw=clean_value(row['AvgW']),
                    avgl=clean_value(row['AvgL']),
                ))

            except Player.DoesNotExist as e:
                self.stderr.write(f"Player not found: {e}")
            except Tournament.DoesNotExist as e:
                self.stderr.write(f"Tournament not found: {e}")
            except IntegrityError as e:
                self.stderr.write(f"Integrity error: {e}")
            except Exception as e:
                self.stderr.write(f"An error occurred: {e}")
        Match.objects.bulk_create(matches)
        self.stdout.write(self.style.SUCCESS("Matches successfully loaded!"))
