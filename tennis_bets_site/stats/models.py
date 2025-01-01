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
    w_2ndWon = models.IntegerField(null=True, blank=True)
    w_SvGms = models.IntegerField(null=True, blank=True)

    l_svpt = models.IntegerField(null=True, blank=True)
    l_1stIn = models.IntegerField(null=True, blank=True)
    l_1stWon = models.IntegerField(null=True, blank=True)
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

    def __str__(self):
        return f"{self.winner.name} vs {self.loser.name} on {self.date}"
