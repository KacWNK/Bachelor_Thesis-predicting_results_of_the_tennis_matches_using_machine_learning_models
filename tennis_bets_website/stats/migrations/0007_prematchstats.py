# Generated by Django 5.1.4 on 2025-01-02 18:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0006_match_uncertain_match_winner_model_prediction_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreMatchStats',
            fields=[
                ('match', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='pre_match_stats', serialize=False, to='stats.match')),
                ('w_ace_avg', models.FloatField(blank=True, null=True)),
                ('l_ace_avg', models.FloatField(blank=True, null=True)),
                ('w_CO_ace_avg', models.FloatField(blank=True, null=True)),
                ('l_CO_ace_avg', models.FloatField(blank=True, null=True)),
                ('w_df_avg', models.FloatField(blank=True, null=True)),
                ('l_df_avg', models.FloatField(blank=True, null=True)),
                ('w_CO_df_avg', models.FloatField(blank=True, null=True)),
                ('l_CO_df_avg', models.FloatField(blank=True, null=True)),
                ('winner_1st_serve_in_pct_avg', models.FloatField(blank=True, null=True)),
                ('loser_1st_serve_in_pct_avg', models.FloatField(blank=True, null=True)),
                ('winner_2nd_serve_win_pct_avg', models.FloatField(blank=True, null=True)),
                ('loser_2nd_serve_win_pct_avg', models.FloatField(blank=True, null=True)),
                ('winner_service_games_won_pct_avg', models.FloatField(blank=True, null=True)),
                ('loser_service_games_won_pct_avg', models.FloatField(blank=True, null=True)),
                ('non_CO_uncertainty', models.FloatField(blank=True, null=True)),
                ('CO_uncertainty', models.FloatField(blank=True, null=True)),
                ('elo_winner', models.FloatField(blank=True, null=True)),
                ('elo_loser', models.FloatField(blank=True, null=True)),
                ('surface_elo_winner', models.FloatField(blank=True, null=True)),
                ('surface_elo_loser', models.FloatField(blank=True, null=True)),
                ('blended_elo_winner', models.FloatField(blank=True, null=True)),
                ('blended_elo_loser', models.FloatField(blank=True, null=True)),
                ('winner_fatigue_score', models.FloatField(blank=True, null=True)),
                ('loser_fatigue_score', models.FloatField(blank=True, null=True)),
                ('winner_injury_score', models.FloatField(blank=True, null=True)),
                ('loser_injury_score', models.FloatField(blank=True, null=True)),
                ('winner_h2h_wins', models.IntegerField(blank=True, null=True)),
                ('loser_h2h_wins', models.IntegerField(blank=True, null=True)),
                ('winner_h2h_surface_wins', models.IntegerField(blank=True, null=True)),
                ('loser_h2h_surface_wins', models.IntegerField(blank=True, null=True)),
                ('winner_total_wins_tournament_history', models.IntegerField(blank=True, null=True)),
                ('winner_total_losses_tournament_history', models.IntegerField(blank=True, null=True)),
                ('loser_total_wins_tournament_history', models.IntegerField(blank=True, null=True)),
                ('loser_total_losses_tournament_history', models.IntegerField(blank=True, null=True)),
                ('winner_win_pct_last_10', models.FloatField(blank=True, null=True)),
                ('loser_win_pct_last_10', models.FloatField(blank=True, null=True)),
                ('winner_win_pct_last_10_surface', models.FloatField(blank=True, null=True)),
                ('loser_win_pct_last_10_surface', models.FloatField(blank=True, null=True)),
                ('tournament_country', models.CharField(blank=True, max_length=100, null=True)),
                ('winner_home', models.BooleanField(default=False)),
                ('loser_home', models.BooleanField(default=False)),
                ('Round_Num', models.IntegerField(blank=True, null=True)),
                ('Winner_Set_Diff_Tournament', models.IntegerField(blank=True, null=True)),
                ('Winner_Game_Diff_Tournament', models.IntegerField(blank=True, null=True)),
                ('Loser_Set_Diff_Tournament', models.IntegerField(blank=True, null=True)),
                ('Loser_Game_Diff_Tournament', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
