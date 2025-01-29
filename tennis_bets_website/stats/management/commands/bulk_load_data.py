import pandas as pd
from django.core.management.base import BaseCommand
from stats.models import Player, Match, Tournament, PreMatchStats
from django.db.utils import IntegrityError
import os


class Command(BaseCommand):
    help = "Load data from CSV files into the database"

    def handle(self, *args, **kwargs):
        data_dir = os.path.join(os.path.dirname(__file__), '../../data')
        # Load Players
        players_path = os.path.join(data_dir, 'players.csv')
        players_df = pd.read_csv(players_path)

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
                level=row['tournament_level'],
                surface=row['Surface'],
                indoor_or_outdoor=row['indoor_or_outdoor']
            ))
        Tournament.objects.bulk_create(tournaments, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"{len(tournaments)} tournaments successfully loaded!"))

        # Load Matches
        matches_path = os.path.join(data_dir, 'matches.csv')
        matches_df = pd.read_csv(matches_path)

        def clean_value(value, default=None):
            if pd.isnull(value):
                return default
            return value

        matches_df['date'] = pd.to_datetime(matches_df['date'], errors='coerce')

        matches = []
        for index, row in matches_df.iterrows():
            try:
                winner = Player.objects.get(player_id=row['winner_id'])
                loser = Player.objects.get(player_id=row['loser_id'])
                tournament = Tournament.objects.get(tournament_id=row['tournament_id'])

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
                    l_svpt=clean_value(row['l_svpt']),
                    w_1stIn=clean_value(row['w_1stIn']),
                    l_1stIn=clean_value(row['l_1stIn']),
                    w_1stWon=clean_value(row['w_1stWon']),
                    l_1stWon=clean_value(row['l_1stWon']),
                    w_2ndIn=clean_value(row['w_2ndIn']),
                    w_2ndWon=clean_value(row['w_2ndWon']),
                    l_2ndIn=clean_value(row['l_2ndIn']),
                    l_2ndWon=clean_value(row['l_2ndWon']),
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

                    winner_model_prediction=clean_value(row['winner_model_prediction']),
                    winner_odds_prediction=clean_value(row['winner_odds_prediction']),
                    uncertain=clean_value(row['uncertain']),

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


        # Load Pre match stats
        pre_match_stats_path = os.path.join(data_dir, 'pre-match_stats.csv')
        pre_match_stats_df = pd.read_csv(pre_match_stats_path)

        pre_match_stats_df['date'] = pd.to_datetime(matches_df['date'], errors='coerce')
        pre_match_stats = []
        for index, row in pre_match_stats_df.iterrows():
            try:
                match = Match.objects.get(match_id=row['match_id'])
                pre_match_stats.append(PreMatchStats(
                    match=match,
                    w_ace_avg=clean_value(row['w_ace_avg']),
                    l_ace_avg=clean_value(row['l_ace_avg']),
                    w_CO_ace_avg=clean_value(row['w_CO_ace_avg']),
                    l_CO_ace_avg=clean_value(row['l_CO_ace_avg']),
                    w_df_avg=clean_value(row['w_df_avg']),
                    l_df_avg=clean_value(row['l_df_avg']),
                    w_CO_df_avg=clean_value(row['w_CO_df_avg']),
                    l_CO_df_avg=clean_value(row['l_CO_df_avg']),
                    w_2ndIn_avg=clean_value(row['w_2ndIn_avg']),
                    l_2ndIn_avg=clean_value(row['l_2ndIn_avg']),
                    w_CO_2ndIn_avg=clean_value(row['w_CO_2ndIn_avg']),
                    l_CO_2ndIn_avg=clean_value(row['l_CO_2ndIn_avg']),

                    winner_1st_serve_in_pct_avg=clean_value(row['winner_1st_serve_in_pct_avg']),
                    loser_1st_serve_in_pct_avg=clean_value(row['loser_1st_serve_in_pct_avg']),
                    winner_CO_1st_serve_in_pct_avg=clean_value(row['winner_CO_1st_serve_in_pct_avg']),
                    loser_CO_1st_serve_in_pct_avg=clean_value(row['loser_CO_1st_serve_in_pct_avg']),

                    winner_1st_serve_win_pct_avg=clean_value(row['winner_1st_serve_win_pct_avg']),
                    loser_1st_serve_win_pct_avg=clean_value(row['loser_1st_serve_win_pct_avg']),
                    winner_CO_1st_serve_win_pct_avg=clean_value(row['winner_CO_1st_serve_win_pct_avg']),
                    loser_CO_1st_serve_win_pct_avg=clean_value(row['loser_CO_1st_serve_win_pct_avg']),

                    winner_2nd_serve_in_pct_avg=clean_value(row['winner_2nd_serve_in_pct_avg']),
                    loser_2nd_serve_in_pct_avg=clean_value(row['loser_2nd_serve_in_pct_avg']),
                    winner_CO_2nd_serve_in_pct_avg=clean_value(row['winner_CO_2nd_serve_in_pct_avg']),
                    loser_CO_2nd_serve_in_pct_avg=clean_value(row['loser_CO_2nd_serve_in_pct_avg']),

                    winner_2nd_serve_win_pct_avg=clean_value(row['winner_2nd_serve_win_pct_avg']),
                    loser_2nd_serve_win_pct_avg=clean_value(row['loser_2nd_serve_win_pct_avg']),
                    winner_CO_2nd_serve_win_pct_avg=clean_value(row['winner_CO_2nd_serve_win_pct_avg']),
                    loser_CO_2nd_serve_win_pct_avg=clean_value(row['loser_CO_2nd_serve_win_pct_avg']),

                    winner_service_games_won_pct_avg=clean_value(row['winner_service_games_won_pct_avg']),
                    loser_service_games_won_pct_avg=clean_value(row['loser_service_games_won_pct_avg']),
                    winner_CO_service_games_won_pct_avg=clean_value(row['winner_CO_service_games_won_pct_avg']),
                    loser_CO_service_games_won_pct_avg=clean_value(row['loser_CO_service_games_won_pct_avg']),

                    winner_1st_serve_return_win_pct_avg=clean_value(row['winner_1st_serve_return_win_pct_avg']),
                    loser_1st_serve_return_win_pct_avg=clean_value(row['loser_1st_serve_return_win_pct_avg']),
                    winner_CO_1st_serve_return_win_pct_avg=clean_value(row['winner_CO_1st_serve_return_win_pct_avg']),
                    loser_CO_1st_serve_return_win_pct_avg=clean_value(row['loser_CO_1st_serve_return_win_pct_avg']),

                    winner_2nd_serve_return_win_pct_avg=clean_value(row['winner_2nd_serve_return_win_pct_avg']),
                    loser_2nd_serve_return_win_pct_avg=clean_value(row['loser_2nd_serve_return_win_pct_avg']),
                    winner_CO_2nd_serve_return_win_pct_avg=clean_value(row['winner_CO_2nd_serve_return_win_pct_avg']),
                    loser_CO_2nd_serve_return_win_pct_avg=clean_value(row['loser_CO_2nd_serve_return_win_pct_avg']),

                    winner_return_games_win_pct_avg=clean_value(row['winner_return_games_win_pct_avg']),
                    loser_return_games_win_pct_avg=clean_value(row['loser_return_games_win_pct_avg']),
                    winner_CO_return_games_win_pct_avg=clean_value(row['winner_CO_return_games_win_pct_avg']),
                    loser_CO_return_games_win_pct_avg=clean_value(row['loser_CO_return_games_win_pct_avg']),

                    winner_bp_won_pct_avg=clean_value(row['winner_bp_won_pct_avg']),
                    loser_bp_won_pct_avg=clean_value(row['loser_bp_won_pct_avg']),
                    winner_CO_bp_won_pct_avg=clean_value(row['winner_CO_bp_won_pct_avg']),
                    loser_CO_bp_won_pct_avg=clean_value(row['loser_CO_bp_won_pct_avg']),

                    winner_bp_saved_pct_avg=clean_value(row['winner_bp_saved_pct_avg']),
                    loser_bp_saved_pct_avg=clean_value(row['loser_bp_saved_pct_avg']),
                    winner_CO_bp_saved_pct_avg=clean_value(row['winner_CO_bp_saved_pct_avg']),
                    loser_CO_bp_saved_pct_avg=clean_value(row['loser_CO_bp_saved_pct_avg']),
                    non_CO_uncertainty=clean_value(row['non_CO_uncertainty']),
                    CO_uncertainty=clean_value(row['CO_uncertainty']),
                    elo_winner=clean_value(row['elo_winner']),
                    elo_loser=clean_value(row['elo_loser']),
                    surface_elo_winner=clean_value(row['surface_elo_winner']),
                    surface_elo_loser=clean_value(row['surface_elo_loser']),
                    blended_elo_winner=clean_value(row['blended_elo_winner']),
                    blended_elo_loser=clean_value(row['blended_elo_loser']),
                    winner_fatigue_score=clean_value(row['winner_fatigue_score']),
                    loser_fatigue_score=clean_value(row['loser_fatigue_score']),
                    winner_h2h_wins=clean_value(row['winner_h2h_wins'], default=0),
                    loser_h2h_wins=clean_value(row['loser_h2h_wins'], default=0),
                    winner_h2h_surface_wins=clean_value(row['winner_h2h_surface_wins'], default=0),
                    loser_h2h_surface_wins=clean_value(row['loser_h2h_surface_wins'], default=0),
                    winner_home=clean_value(row['winner_home'], default=False),
                    loser_home=clean_value(row['loser_home'], default=False),
                    winner_injury_score=clean_value(row['winner_injury_score']),
                    loser_injury_score=clean_value(row['loser_injury_score']),
                    winner_win_pct_last_10=clean_value(row['winner_win_pct_last_10']),
                    loser_win_pct_last_10=clean_value(row['loser_win_pct_last_10']),
                    winner_win_pct_last_10_surface=clean_value(row['winner_win_pct_last_10_surface']),
                    loser_win_pct_last_10_surface=clean_value(row['loser_win_pct_last_10_surface']),
                    Round_Num=clean_value(row['Round_Num']),
                    Winner_Set_Diff_Tournament=clean_value(row['Winner_Set_Diff_Tournament']),
                    Winner_Game_Diff_Tournament=clean_value(row['Winner_Game_Diff_Tournament']),
                    Loser_Set_Diff_Tournament=clean_value(row['Loser_Set_Diff_Tournament']),
                    Loser_Game_Diff_Tournament=clean_value(row['Loser_Game_Diff_Tournament']),
                    winner_total_wins_tournament_history=clean_value(row['winner_total_wins_tournament_history']),
                    winner_total_losses_tournament_history=clean_value(row['winner_total_losses_tournament_history']),
                    loser_total_wins_tournament_history=clean_value(row['loser_total_wins_tournament_history']),
                    loser_total_losses_tournament_history=clean_value(row['loser_total_losses_tournament_history'])
                ))
            except Match.DoesNotExist:
                print(f"Match ID {row['match_id']} not found, skipping.")
            except Exception as e:
                print(f"Error processing row {index}: {str(e)}")
        PreMatchStats.objects.bulk_create(pre_match_stats)

        print(f"Inserted {len(pre_match_stats)} pre-match stats into the database.")

