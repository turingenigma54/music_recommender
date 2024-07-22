from django.urls import path
from .views import HomeView, SearchView, RecommendationsView, RandomRecommendationView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('recommendations/', RecommendationsView.as_view(), name='recommendations'),
    path('random-recommendation/', RandomRecommendationView.as_view(), name='random_recommendation'),
]