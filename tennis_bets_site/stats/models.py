from django.db import models


class Player(models.Model):
    player_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    rank = models.IntegerField(null=True, blank=True)
    age = models.FloatField(null=True, blank=True)  # Allow decimals for more accuracy
    hand = models.CharField(max_length=10, null=True, blank=True)  # Left or Right

    def __str__(self):
        return self.name


class Tournament(models.Model):
    tournament_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    level = models.CharField(max_length=50, null=True, blank=True)
    draw_size = models.IntegerField(null=True, blank=True)
    surface = models.CharField(max_length=50, null=True, blank=True)
    indoor_or_outdoor = models.CharField(max_length=50, null=True, blank=True)


class Match(models.Model):
    match_id = models.CharField(max_length=100, primary_key=True)  # Unique ID for each match
    date = models.DateField()  # Match date
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="matches")  # Tournament link
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="wins")  # Winning player
    loser = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="losses")  # Losing player

    # Match context
    round = models.CharField(max_length=50, null=True, blank=True)  # Round of the match
    indoor_or_outdoor = models.CharField(max_length=20, null=True, blank=True)  # Indoor/Outdoor
    best_of = models.IntegerField(null=True, blank=True)  # Best of 3 or 5 sets
    minutes = models.IntegerField(null=True, blank=True)  # Match duration in minutes

    # Player seeds and entries
    winner_seed = models.IntegerField(null=True, blank=True)
    loser_seed = models.IntegerField(null=True, blank=True)
    winner_entry = models.CharField(max_length=20, null=True, blank=True)
    loser_entry = models.CharField(max_length=20, null=True, blank=True)

    # Player ranks
    winner_rank = models.IntegerField(null=True, blank=True)
    loser_rank = models.IntegerField(null=True, blank=True)
    winner_rank_points = models.IntegerField(null=True, blank=True)
    loser_rank_points = models.IntegerField(null=True, blank=True)

    # Player ages
    winner_age = models.FloatField(null=True, blank=True)
    loser_age = models.FloatField(null=True, blank=True)

    # Set scores
    w1 = models.IntegerField(null=True, blank=True)
    l1 = models.IntegerField(null=True, blank=True)
    w2 = models.IntegerField(null=True, blank=True)
    l2 = models.IntegerField(null=True, blank=True)
    w3 = models.IntegerField(null=True, blank=True)
    l3 = models.IntegerField(null=True, blank=True)
    w4 = models.IntegerField(null=True, blank=True)
    l4 = models.IntegerField(null=True, blank=True)
    w5 = models.IntegerField(null=True, blank=True)
    l5 = models.IntegerField(null=True, blank=True)

    # Total sets won
    wsets = models.IntegerField(null=True, blank=True)
    lsets = models.IntegerField(null=True, blank=True)

    # Performance stats
    w_ace = models.IntegerField(null=True, blank=True)
    l_ace = models.IntegerField(null=True, blank=True)
    w_df = models.IntegerField(null=True, blank=True)
    l_df = models.IntegerField(null=True, blank=True)
    w_bpSaved = models.IntegerField(null=True, blank=True)
    l_bpSaved = models.IntegerField(null=True, blank=True)
    w_bpFaced = models.IntegerField(null=True, blank=True)
    l_bpFaced = models.IntegerField(null=True, blank=True)

    w_svpt = models.IntegerField(null=True, blank=True)
    w_1stIn = models.IntegerField(null=True, blank=True)
    w_1stWon = models.IntegerField(null=True, blank=True)
    w_2ndIn = models.IntegerField(null=True, blank=True)
    w_2ndWon = models.IntegerField(null=True, blank=True)
    w_SvGms = models.IntegerField(null=True, blank=True)

    l_svpt = models.IntegerField(null=True, blank=True)
    l_1stIn = models.IntegerField(null=True, blank=True)
    l_1stWon = models.IntegerField(null=True, blank=True)
    l_2ndIn = models.IntegerField(null=True, blank=True)
    l_2ndWon = models.IntegerField(null=True, blank=True)
    l_SvGms = models.IntegerField(null=True, blank=True)

    winner_1st_serve_in_pct = models.FloatField(null=True, blank=True)
    winner_1st_serve_win_pct = models.FloatField(null=True, blank=True)
    winner_2nd_serve_in_pct = models.FloatField(null=True, blank=True)
    winner_2nd_serve_win_pct = models.FloatField(null=True, blank=True)
    winner_service_games_won_pct = models.FloatField(null=True, blank=True)

    loser_1st_serve_in_pct = models.FloatField(null=True, blank=True)
    loser_1st_serve_win_pct = models.FloatField(null=True, blank=True)
    loser_2nd_serve_in_pct = models.FloatField(null=True, blank=True)
    loser_2nd_serve_win_pct = models.FloatField(null=True, blank=True)
    loser_service_games_won_pct = models.FloatField(null=True, blank=True)

    winner_1st_serve_return_win_pct = models.FloatField(null=True, blank=True)
    winner_2nd_serve_return_win_pct = models.FloatField(null=True, blank=True)
    winner_return_games_win_pct = models.FloatField(null=True, blank=True)

    loser_1st_serve_return_win_pct = models.FloatField(null=True, blank=True)
    loser_2nd_serve_return_win_pct = models.FloatField(null=True, blank=True)
    loser_return_games_win_pct = models.FloatField(null=True, blank=True)

    winner_bp_won_pct = models.FloatField(null=True, blank=True)
    loser_bp_won_pct = models.FloatField(null=True, blank=True)
    winner_bp_saved_pct = models.FloatField(null=True, blank=True)
    loser_bp_saved_pct = models.FloatField(null=True, blank=True)

    # Miscellaneous
    comment = models.TextField(null=True, blank=True)
    avgw = models.FloatField(null=True, blank=True)  # Average odds for winner
    avgl = models.FloatField(null=True, blank=True)  # Average odds for loser

    # Model
    winner_model_prediction = models.FloatField(null=True, blank=True)
    winner_odds_prediction = models.FloatField(null=True, blank=True)
    uncertain = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.winner.name} vs {self.loser.name} on {self.date}"


class PreMatchStats(models.Model):
    match = models.OneToOneField(
        Match,
        on_delete=models.CASCADE,
        related_name="pre_match_stats",
        primary_key=True,
    )

    # --- Statistical Features ---
    w_ace_avg = models.FloatField(null=True, blank=True)
    l_ace_avg = models.FloatField(null=True, blank=True)
    w_CO_ace_avg = models.FloatField(null=True, blank=True)
    l_CO_ace_avg = models.FloatField(null=True, blank=True)

    w_df_avg = models.FloatField(null=True, blank=True)
    l_df_avg = models.FloatField(null=True, blank=True)
    w_CO_df_avg = models.FloatField(null=True, blank=True)
    l_CO_df_avg = models.FloatField(null=True, blank=True)

    w_2ndIn_avg = models.FloatField(null=True, blank=True)
    l_2ndIn_avg = models.FloatField(null=True, blank=True)
    w_CO_2ndIn_avg = models.FloatField(null=True, blank=True)
    l_CO_2ndIn_avg = models.FloatField(null=True, blank=True)

    winner_1st_serve_in_pct_avg = models.FloatField(null=True, blank=True)
    loser_1st_serve_in_pct_avg = models.FloatField(null=True, blank=True)
    winner_CO_1st_serve_in_pct_avg = models.FloatField(null=True, blank=True)
    loser_CO_1st_serve_in_pct_avg = models.FloatField(null=True, blank=True)

    winner_1st_serve_win_pct_avg = models.FloatField(null=True, blank=True)
    loser_1st_serve_win_pct_avg = models.FloatField(null=True, blank=True)
    winner_CO_1st_serve_win_pct_avg = models.FloatField(null=True, blank=True)
    loser_CO_1st_serve_win_pct_avg = models.FloatField(null=True, blank=True)

    winner_2nd_serve_in_pct_avg = models.FloatField(null=True, blank=True)
    loser_2nd_serve_in_pct_avg = models.FloatField(null=True, blank=True)
    winner_CO_2nd_serve_in_pct_avg = models.FloatField(null=True, blank=True)
    loser_CO_2nd_serve_in_pct_avg = models.FloatField(null=True, blank=True)

    winner_2nd_serve_win_pct_avg = models.FloatField(null=True, blank=True)
    loser_2nd_serve_win_pct_avg = models.FloatField(null=True, blank=True)
    winner_CO_2nd_serve_win_pct_avg = models.FloatField(null=True, blank=True)
    loser_CO_2nd_serve_win_pct_avg = models.FloatField(null=True, blank=True)

    # Service game statistics
    winner_service_games_won_pct_avg = models.FloatField(null=True, blank=True)
    loser_service_games_won_pct_avg = models.FloatField(null=True, blank=True)
    winner_CO_service_games_won_pct_avg = models.FloatField(null=True, blank=True)
    loser_CO_service_games_won_pct_avg = models.FloatField(null=True, blank=True)

    # Return statistics
    winner_1st_serve_return_win_pct_avg = models.FloatField(null=True, blank=True)
    loser_1st_serve_return_win_pct_avg = models.FloatField(null=True, blank=True)
    winner_CO_1st_serve_return_win_pct_avg = models.FloatField(null=True, blank=True)
    loser_CO_1st_serve_return_win_pct_avg = models.FloatField(null=True, blank=True)

    winner_2nd_serve_return_win_pct_avg = models.FloatField(null=True, blank=True)
    loser_2nd_serve_return_win_pct_avg = models.FloatField(null=True, blank=True)
    winner_CO_2nd_serve_return_win_pct_avg = models.FloatField(null=True, blank=True)
    loser_CO_2nd_serve_return_win_pct_avg = models.FloatField(null=True, blank=True)

    winner_return_games_win_pct_avg = models.FloatField(null=True, blank=True)
    loser_return_games_win_pct_avg = models.FloatField(null=True, blank=True)
    winner_CO_return_games_win_pct_avg = models.FloatField(null=True, blank=True)
    loser_CO_return_games_win_pct_avg = models.FloatField(null=True, blank=True)

    # Break point statistics
    winner_bp_won_pct_avg = models.FloatField(null=True, blank=True)
    loser_bp_won_pct_avg = models.FloatField(null=True, blank=True)
    winner_CO_bp_won_pct_avg = models.FloatField(null=True, blank=True)
    loser_CO_bp_won_pct_avg = models.FloatField(null=True, blank=True)

    winner_bp_saved_pct_avg = models.FloatField(null=True, blank=True)
    loser_bp_saved_pct_avg = models.FloatField(null=True, blank=True)
    winner_CO_bp_saved_pct_avg = models.FloatField(null=True, blank=True)
    loser_CO_bp_saved_pct_avg = models.FloatField(null=True, blank=True)

    # --- Uncertainty and Elo Ratings ---
    non_CO_uncertainty = models.FloatField(null=True, blank=True)
    CO_uncertainty = models.FloatField(null=True, blank=True)

    elo_winner = models.FloatField(null=True, blank=True)
    elo_loser = models.FloatField(null=True, blank=True)

    surface_elo_winner = models.FloatField(null=True, blank=True)
    surface_elo_loser = models.FloatField(null=True, blank=True)

    blended_elo_winner = models.FloatField(null=True, blank=True)
    blended_elo_loser = models.FloatField(null=True, blank=True)

    # --- Fatigue and Injuries ---
    winner_fatigue_score = models.FloatField(null=True, blank=True)
    loser_fatigue_score = models.FloatField(null=True, blank=True)

    winner_injury_score = models.FloatField(null=True, blank=True)
    loser_injury_score = models.FloatField(null=True, blank=True)

    # --- H2H Metrics ---
    winner_h2h_wins = models.IntegerField(null=True, blank=True)
    loser_h2h_wins = models.IntegerField(null=True, blank=True)
    winner_h2h_surface_wins = models.IntegerField(null=True, blank=True)
    loser_h2h_surface_wins = models.IntegerField(null=True, blank=True)

    # --- Historical Tournament Stats ---
    winner_total_wins_tournament_history = models.IntegerField(null=True, blank=True)
    winner_total_losses_tournament_history = models.IntegerField(null=True, blank=True)
    loser_total_wins_tournament_history = models.IntegerField(null=True, blank=True)
    loser_total_losses_tournament_history = models.IntegerField(null=True, blank=True)

    # --- Win Percentages ---
    winner_win_pct_last_10 = models.FloatField(null=True, blank=True)
    loser_win_pct_last_10 = models.FloatField(null=True, blank=True)
    winner_win_pct_last_10_surface = models.FloatField(null=True, blank=True)
    loser_win_pct_last_10_surface = models.FloatField(null=True, blank=True)

    # --- Additional Context ---
    tournament_country = models.CharField(max_length=100, null=True, blank=True)
    winner_home = models.BooleanField(default=False)
    loser_home = models.BooleanField(default=False)

    # --- Derived Metrics ---
    Round_Num = models.IntegerField(null=True, blank=True)
    Winner_Set_Diff_Tournament = models.IntegerField(null=True, blank=True)
    Winner_Game_Diff_Tournament = models.IntegerField(null=True, blank=True)
    Loser_Set_Diff_Tournament = models.IntegerField(null=True, blank=True)
    Loser_Game_Diff_Tournament = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Pre-Match Stats for Match {self.match.match_id}"
