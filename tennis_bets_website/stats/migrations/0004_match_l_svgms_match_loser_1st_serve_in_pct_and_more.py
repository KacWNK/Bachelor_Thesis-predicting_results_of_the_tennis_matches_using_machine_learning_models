# Generated by Django 5.1.4 on 2024-12-22 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_tournament_remove_match_surface_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='l_SvGms',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='loser_1st_serve_in_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='loser_1st_serve_return_win_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='loser_1st_serve_win_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='loser_2nd_serve_in_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='loser_2nd_serve_return_win_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='loser_2nd_serve_win_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='loser_bp_saved_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='loser_bp_won_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='loser_return_games_win_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='loser_service_games_won_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='w_1stIn',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='w_1stWon',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='w_2ndWon',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='w_SvGms',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='w_svpt',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='winner_1st_serve_in_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='winner_1st_serve_return_win_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='winner_1st_serve_win_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='winner_2nd_serve_in_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='winner_2nd_serve_return_win_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='winner_2nd_serve_win_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='winner_bp_saved_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='winner_bp_won_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='winner_return_games_win_pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='winner_service_games_won_pct',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
