from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.stats_view, name='stats'),
    path('results/', TemplateView.as_view(template_name='stats/results.html'), name='results'),
    # API URL for match data
    path('api/matches/<str:match_id>/', views.MatchDetailAPI.as_view(), name='match-detail-api'),
    # URL for serving the match detail template
    path('match/<str:match_id>/', TemplateView.as_view(template_name='stats/match_detail.html'), name='match_detail'),
    path('api/h2h-matches/', views.H2HMatchListAPI.as_view(), name='h2h-matches'),
    path('api/pre-match-stats/<str:match_id>/', views.PreMatchStatsAPI.as_view(), name='pre-match-stats-detail'),
    path('api/matches/', views.MatchesByDateAPI.as_view(), name='matches_by_date'),
]
