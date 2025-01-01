from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.stats_view, name='stats'),
    path('player/search/', views.player_search, name='player_search'),
    path('player/<int:player_id>/', views.player_bio, name='player_bio'),
    path('results/', views.results, name='results'),
    # API URL for match data
    path('api/matches/<str:match_id>/', views.MatchDetailAPI.as_view(), name='match-detail-api'),
    # URL for serving the match detail template
    path('match/<str:match_id>/', TemplateView.as_view(template_name='stats/match_detail.html'), name='match_detail')
]
