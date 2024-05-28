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
        # url = "https://api.themoviedb.org/3/configuration"
        url = 'https://api.themoviedb.org/3/search/movie'
        api_key = '79313ab3de3abf8b796b2e7e8a890c6b' 
          # Replace with your actual TMDB API key
        # url = 'https://api.themoviedb.org/3/movie/550/images?language=en-US&include_image_language=en,null'
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3OTMxM2FiM2RlM2FiZjhiNzk2YjJlN2U4YTg5MGM2YiIsInN1YiI6IjY2NGE1OGUxNzUwOTY5OGEwMTFkOWJiOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.xwxzT61osz5AmFPf7biNvycx-iwWIbFdb8wi12LeO4I"
        }
        # Make a GET request to the TMDB API
        response = requests.get(url, params={'api_key': api_key, 'query': movie_name}, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract movie data from the response
            data = response.json()['results']

            poster_urls = [movie['poster_path'] for movie in data if movie.get('poster_path')]
            # Update movie data with poster URLs
            for i, movie in enumerate(data):
                if movie.get('poster_path'):
                    data[i]['poster_url'] = f'https://image.tmdb.org/t/p/w500{movie["poster_path"]}'
                    data[i]['overview'] = movie.get('overview', 'No overview available')
                    movie_id = movie.get('id')
                if movie_id:
                    movie_details_url = f'https://api.themoviedb.org/3/movie/{movie_id}'
                    details_response = requests.get(movie_details_url, params={'api_key': api_key})
                    if details_response.status_code == 200:
                        details_data = details_response.json()
                        data[i]['movie_rating'] = details_data.get('vote_average', 'No rating available')
                    else:
                        data[i]['movie_rating'] = 'No rating available'
                else:
                    data[i]['movie_rating'] = 'No rating available'
        
        else:
            data = []  # Empty list if there's an error

        # Pass the movie data to the template for rendering
        return render(request, 'recommendations/movie_list.html', {'data': data, 'query': movie_name})
        # Updated template path: 'recommendations/movie_list.html'
    else:
        return render(request, 'search.html')