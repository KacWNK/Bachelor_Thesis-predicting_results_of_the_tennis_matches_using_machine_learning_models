from django.shortcuts import render, redirect
from .models import Player, Match
from django.db.models import Q
import datetime
from django.utils.timezone import now
from rest_framework import generics
from .models import Match
from .serializers import MatchSerializer

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


def results(request):
    # Get the selected date from the query string or default to today
    selected_date = request.GET.get('date', None)

    if selected_date:
        try:
            # Parse the selected date string
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date = now().date()  # Fallback to today if parsing fails
    else:
        # Use today's date as the default
        selected_date = now().date()
    print(selected_date)
    # Filter matches by the selected date
    matches = Match.objects.filter(date=selected_date).select_related('tournament', 'winner', 'loser')
    print(matches)
    # Group matches by tournaments
    grouped_matches = {}
    for match in matches:
        tournament = match.tournament
        if tournament not in grouped_matches:
            grouped_matches[tournament] = []
        grouped_matches[tournament].append(match)

    context = {
        'grouped_matches': grouped_matches,
        'selected_date': selected_date,
    }
    return render(request, 'stats/results.html', context)

# def match_detail(request, match_id):
#     match = Match.objects.get(match_id=match_id)
#     return render(request, 'stats/match_detail.html', {'match': match})

class MatchDetailAPI(generics.RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    lookup_field = 'match_id'  # Allows lookup by match_id