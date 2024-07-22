from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import df, get_recommendations_from_file

class HomeView(View):
    def get(self, request):
        return render(request, 'recommender/home.html')

class SearchView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('query', '')
        matching_tracks = df[df['track_name'].str.contains(query, case=False)]['track_name'].tolist()
        return render(request, 'recommender/search.html', {'tracks': matching_tracks, 'query': query})

class RecommendationsView(LoginRequiredMixin, View):
    def get(self, request):
        track_name = request.GET.get('track_name')
        if not track_name:
            return render(request, 'recommender/recommendations.html', {'error': 'No track selected'})

        recommendations = get_recommendations_from_file(track_name, df)
        context = {
            'input_track': track_name,
            'recommendations': recommendations
        }
        return render(request, 'recommender/recommendations.html', context)

class RandomRecommendationView(LoginRequiredMixin, View):
    def get(self, request):
        random_track = df['track_name'].sample().iloc[0]
        recommendations = get_recommendations_from_file(random_track, df)
        context = {
            'input_track': random_track,
            'recommendations': recommendations
        }
        return render(request, 'recommender/recommendations.html', context)