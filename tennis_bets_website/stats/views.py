from django.shortcuts import render, redirect
from .models import Player, Match, PreMatchStats
from django.db.models import Q
import datetime
from django.utils.timezone import now
from rest_framework import generics
from .serializers import MatchSerializer, PreMatchStatsSerializer
from django.utils.safestring import mark_safe
import json
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


def stats_view(request):
    # Most recent matches
    recent_matches = Match.objects.order_by('-date')[:10]

    context = {
        'recent_matches': recent_matches,
    }
    return render(request, 'stats/stats.html', context)


def player_search(request):
    player_name = request.GET.get('player_name')
    if player_name:
        try:
            # Find the player (case-insensitive search)
            player = Player.objects.get(name__iexact=player_name)
            # Redirect to the player's bio page
            return redirect('player_bio', player_id=player.player_id)
        except Player.DoesNotExist:
            # If the player doesn't exist, return to the stats page with an error
            return redirect('stats')
    return redirect('stats')


def player_bio(request, player_id):
    try:
        # Get the player object
        player = Player.objects.get(player_id=player_id)

        # Get recent matches (both won and lost)
        recent_matches = Match.objects.filter(
            Q(winner=player) | Q(loser=player)
        ).order_by('-date')[:10]  # Limit to the last 10 matches

        context = {
            'player': player,
            'recent_matches': recent_matches,
        }
        return render(request, 'stats/player_bio.html', context)
    except Player.DoesNotExist:
        return redirect('stats')  # Redirect to stats page if the player is not found


# def results(request):
#     # Get the selected date from the query string or default to today
#     selected_date = request.GET.get('date', None)
#
#     if selected_date:
#         try:
#             # Parse the selected date string
#             selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
#         except ValueError:
#             selected_date = now().date()  # Fallback to today if parsing fails
#     else:
#         # Use today's date as the default
#         selected_date = now().date()
#     # Filter matches by the selected date
#     matches = Match.objects.filter(date=selected_date).select_related('tournament', 'winner', 'loser')
#     # Group matches by tournaments
#     grouped_matches = {}
#     for match in matches:
#         tournament = match.tournament
#         if tournament not in grouped_matches:
#             grouped_matches[tournament] = []
#         grouped_matches[tournament].append(match)
#
#     grouped_matches_serializable = {
#         str(tournament): matches for tournament, matches in grouped_matches.items()
#     }
#     context = {
#         'grouped_matches': mark_safe(json.dumps(grouped_matches_serializable)),
#         'selected_date': selected_date,
#     }
#     return render(request, 'stats/results.html', context)


class MatchDetailAPI(generics.RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    lookup_field = 'match_id'  # Allows lookup by match_id


class H2HMatchListAPI(generics.ListAPIView):
    serializer_class = MatchSerializer

    def get_queryset(self):
        # Parse player IDs safely
        try:
            player1_id = str(self.request.query_params.get('player1').strip())
            player2_id = str(self.request.query_params.get('player2').strip())
        except (TypeError, ValueError, AttributeError):
            return Match.objects.none()


        # Query matches by ForeignKey references
        queryset = Match.objects.filter(
            Q(winner=player1_id, loser=player2_id) |
            Q(winner=player2_id, loser=player1_id)
        ).order_by('-date')

        return queryset

class PreMatchStatsAPI(generics.RetrieveAPIView):
    queryset = PreMatchStats.objects.select_related('match')
    serializer_class = PreMatchStatsSerializer
    lookup_field = 'match_id'  # Lookup based on match_id


class MatchesByDateAPI(generics.ListAPIView):
    serializer_class = MatchSerializer

    def get_queryset(self):
        # Get the date from query parameters
        date = self.request.query_params.get('date', None)
        if not date:
            raise ValidationError({'date': 'This query parameter is required.'})

        # Filter matches by date
        return Match.objects.filter(date=date)  # Adjust 'date' to your model's field name

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Group matches by tournament
        grouped_matches = {}
        for match in queryset:
            tournament_name = str(match.tournament.name)  # Adjust based on your model
            if tournament_name not in grouped_matches:
                grouped_matches[tournament_name] = []
            grouped_matches[tournament_name].append(self.get_serializer(match).data)

        return Response({"grouped_matches": grouped_matches})