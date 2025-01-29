from django.shortcuts import render, redirect
from .models import Player, Match, PreMatchStats
from django.db.models import Q
from rest_framework import generics
from .serializers import MatchSerializer, PreMatchStatsSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


def stats_view(request):
    recent_matches = Match.objects.order_by('-date')[:10]

    context = {
        'recent_matches': recent_matches,
    }
    return render(request, 'stats/stats.html', context)


class MatchDetailAPI(generics.RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    lookup_field = 'match_id'


class H2HMatchListAPI(generics.ListAPIView):
    serializer_class = MatchSerializer

    def get_queryset(self):
        try:
            player1_id = str(self.request.query_params.get('player1').strip())
            player2_id = str(self.request.query_params.get('player2').strip())
        except (TypeError, ValueError, AttributeError):
            return Match.objects.none()

        queryset = Match.objects.filter(
            Q(winner=player1_id, loser=player2_id) |
            Q(winner=player2_id, loser=player1_id)
        ).order_by('-date')

        return queryset


class PreMatchStatsAPI(generics.RetrieveAPIView):
    queryset = PreMatchStats.objects.select_related('match')
    serializer_class = PreMatchStatsSerializer
    lookup_field = 'match_id'


class MatchesByDateAPI(generics.ListAPIView):
    serializer_class = MatchSerializer

    def get_queryset(self):
        date = self.request.query_params.get('date', None)
        if not date:
            raise ValidationError({'date': 'This query parameter is required.'})

        return Match.objects.filter(date=date)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        grouped_matches = {}
        for match in queryset:
            tournament_name = str(match.tournament.name)
            if tournament_name not in grouped_matches:
                grouped_matches[tournament_name] = []
            grouped_matches[tournament_name].append(self.get_serializer(match).data)

        return Response({"grouped_matches": grouped_matches})