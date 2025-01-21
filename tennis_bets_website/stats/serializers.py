from rest_framework import serializers
from .models import Match, PreMatchStats


class MatchSerializer(serializers.ModelSerializer):
    winner_name = serializers.CharField(source='winner.name')  # Nested field for winner's name
    loser_name = serializers.CharField(source='loser.name')  # Nested field for loser's name
    surface = serializers.CharField(source='tournament.surface')  # Pull surface via relationship
    tournament_name = serializers.CharField(source='tournament.name')

    class Meta:
        model = Match
        fields = ['match_id', 'winner_name', 'loser_name', 'tournament_name', 'date', 'tournament_id', 'round', 'indoor_or_outdoor', 'best_of', 'minutes', 'winner_id', 'loser_id',
'winner_seed', 'loser_seed', 'winner_entry', 'loser_entry', 'winner_rank', 'loser_rank', 'winner_rank_points',
'loser_rank_points', 'winner_age', 'loser_age', 'w1', 'l1', 'w2', 'l2', 'w3', 'l3', 'w4', 'l4', 'w5', 'l5',
'wsets', 'lsets', 'w_ace', 'l_ace', 'w_df', 'l_df', 'w_bpSaved', 'l_bpSaved', 'w_bpFaced', 'l_bpFaced', 'w_svpt',
'w_1stIn', 'w_1stWon', 'w_2ndIn', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndIn',
'l_2ndWon', 'winner_1st_serve_in_pct', 'winner_1st_serve_win_pct', 'winner_2nd_serve_in_pct', 'winner_2nd_serve_win_pct',
'winner_service_games_won_pct', 'loser_1st_serve_in_pct', 'loser_1st_serve_win_pct', 'loser_2nd_serve_in_pct',
'loser_2nd_serve_win_pct', 'loser_service_games_won_pct', 'winner_1st_serve_return_win_pct',
'winner_2nd_serve_return_win_pct', 'winner_return_games_win_pct', 'loser_1st_serve_return_win_pct',
'loser_2nd_serve_return_win_pct', 'loser_return_games_win_pct', 'winner_bp_won_pct', 'loser_bp_won_pct',
'winner_bp_saved_pct', 'loser_bp_saved_pct', 'l_SvGms', 'comment', 'avgw', 'avgl', 'winner_model_prediction', 'surface',
                  'winner_odds_prediction', 'uncertain', 'scheduled']


class PreMatchStatsSerializer(serializers.ModelSerializer):
    # Match-related fields
    match_id = serializers.CharField(source='match.match_id', read_only=True)
    date = serializers.DateField(source='match.date', read_only=True)

    class Meta:
        model = PreMatchStats
        fields = [
            # Match info
            'match_id', 'date',

            # Serve Stats
            'w_ace_avg', 'l_ace_avg', 'w_CO_ace_avg', 'l_CO_ace_avg',
            'w_df_avg', 'l_df_avg', 'w_CO_df_avg', 'l_CO_df_avg',
            'w_2ndIn_avg', 'l_2ndIn_avg', 'w_CO_2ndIn_avg', 'l_CO_2ndIn_avg',

            # Serve Percentages
            'winner_1st_serve_in_pct_avg', 'loser_1st_serve_in_pct_avg',
            'winner_CO_1st_serve_in_pct_avg', 'loser_CO_1st_serve_in_pct_avg',
            'winner_1st_serve_win_pct_avg', 'loser_1st_serve_win_pct_avg',
            'winner_CO_1st_serve_win_pct_avg', 'loser_CO_1st_serve_win_pct_avg',
            'winner_2nd_serve_in_pct_avg', 'loser_2nd_serve_in_pct_avg',
            'winner_CO_2nd_serve_in_pct_avg', 'loser_CO_2nd_serve_in_pct_avg',
            'winner_2nd_serve_win_pct_avg', 'loser_2nd_serve_win_pct_avg',
            'winner_CO_2nd_serve_win_pct_avg', 'loser_CO_2nd_serve_win_pct_avg',

            # Game and Return Stats
            'winner_service_games_won_pct_avg', 'loser_service_games_won_pct_avg',
            'winner_CO_service_games_won_pct_avg', 'loser_CO_service_games_won_pct_avg',
            'winner_1st_serve_return_win_pct_avg', 'loser_1st_serve_return_win_pct_avg',
            'winner_CO_1st_serve_return_win_pct_avg', 'loser_CO_1st_serve_return_win_pct_avg',
            'winner_2nd_serve_return_win_pct_avg', 'loser_2nd_serve_return_win_pct_avg',
            'winner_CO_2nd_serve_return_win_pct_avg', 'loser_CO_2nd_serve_return_win_pct_avg',
            'winner_return_games_win_pct_avg', 'loser_return_games_win_pct_avg',
            'winner_CO_return_games_win_pct_avg', 'loser_CO_return_games_win_pct_avg',

            # Break Points
            'winner_bp_won_pct_avg', 'loser_bp_won_pct_avg',
            'winner_CO_bp_won_pct_avg', 'loser_CO_bp_won_pct_avg',
            'winner_bp_saved_pct_avg', 'loser_bp_saved_pct_avg',
            'winner_CO_bp_saved_pct_avg', 'loser_CO_bp_saved_pct_avg',

            # Uncertainty Metrics
            'non_CO_uncertainty', 'CO_uncertainty',

            # Elo Ratings
            'elo_winner', 'elo_loser',
            'surface_elo_winner', 'surface_elo_loser',
            'blended_elo_winner', 'blended_elo_loser',

            # Fatigue Scores
            'winner_fatigue_score', 'loser_fatigue_score',

            # Head-to-Head Stats
            'winner_h2h_wins', 'loser_h2h_wins',
            'winner_h2h_surface_wins', 'loser_h2h_surface_wins',

            # Location and Home Advantage
            'tournament_country', 'winner_home', 'loser_home',

            # Injury Flags
            'winner_injury_score', 'loser_injury_score',

            # Recent Performance
            'winner_win_pct_last_10', 'loser_win_pct_last_10',
            'winner_win_pct_last_10_surface', 'loser_win_pct_last_10_surface',

            # Tournament Stats
            'Round_Num',
            'Winner_Set_Diff_Tournament', 'Winner_Game_Diff_Tournament',
            'Loser_Set_Diff_Tournament', 'Loser_Game_Diff_Tournament',
            'winner_total_wins_tournament_history', 'winner_total_losses_tournament_history',
            'loser_total_wins_tournament_history', 'loser_total_losses_tournament_history',
        ]
