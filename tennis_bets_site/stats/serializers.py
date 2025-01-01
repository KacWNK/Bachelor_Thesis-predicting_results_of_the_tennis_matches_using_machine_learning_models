from rest_framework import serializers
from .models import Match


class MatchSerializer(serializers.ModelSerializer):
    winner_name = serializers.CharField(source='winner.name')  # Nested field for winner's name
    loser_name = serializers.CharField(source='loser.name')  # Nested field for loser's name

    class Meta:
        model = Match
        fields = ['match_id', 'winner_name', 'loser_name', 'date', 'tournament_id', 'round', 'indoor_or_outdoor', 'best_of', 'minutes', 'winner_id', 'loser_id',
'winner_seed', 'loser_seed', 'winner_entry', 'loser_entry', 'winner_rank', 'loser_rank', 'winner_rank_points',
'loser_rank_points', 'winner_age', 'loser_age', 'w1', 'l1', 'w2', 'l2', 'w3', 'l3', 'w4', 'l4', 'w5', 'l5',
'wsets', 'lsets', 'w_ace', 'l_ace', 'w_df', 'l_df', 'w_bpSaved', 'l_bpSaved', 'w_bpFaced', 'l_bpFaced', 'w_svpt',
'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon',
'l_2ndWon', 'winner_1st_serve_in_pct', 'winner_1st_serve_win_pct', 'winner_2nd_serve_in_pct', 'winner_2nd_serve_win_pct',
'winner_service_games_won_pct', 'loser_1st_serve_in_pct', 'loser_1st_serve_win_pct', 'loser_2nd_serve_in_pct',
'loser_2nd_serve_win_pct', 'loser_service_games_won_pct', 'winner_1st_serve_return_win_pct',
'winner_2nd_serve_return_win_pct', 'winner_return_games_win_pct', 'loser_1st_serve_return_win_pct',
'loser_2nd_serve_return_win_pct', 'loser_return_games_win_pct', 'winner_bp_won_pct', 'loser_bp_won_pct',
'winner_bp_saved_pct', 'loser_bp_saved_pct', 'l_SvGms', 'comment', 'avgw', 'avgl']

