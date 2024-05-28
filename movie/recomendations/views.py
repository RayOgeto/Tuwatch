from django.shortcuts import render
from .models import Movie
import requests

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'recommendations/movie_list.html', {'movies': movies})

def search_results(request):
    if 'movie_name' in request.GET:
        movie_name = request.GET['movie_name']
        # Define TMDB API endpoint and parameters
        url = 'https://api.themoviedb.org/3/search/movie'
        api_key = '79313ab3de3abf8b796b2e7e8a890c6b' 
          # Replace with your actual TMDB API key

        # Make a GET request to the TMDB API
        response = requests.get(url, params={'api_key': api_key, 'query': movie_name})

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract movie data from the response
            data = response.json()['results']
        else:
            data = []  # Empty list if there's an error

        # Pass the movie data to the template for rendering
        return render(request, 'recommendations/movie_list.html', {'data': data, 'query': movie_name})
        # Updated template path: 'recommendations/movie_list.html'
    else:
        return render(request, 'search.html')