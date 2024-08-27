import os
import requests
from django.core.management.base import BaseCommand
from recomendations.models import Movie

class Command(BaseCommand):
    help = 'Fetch movies from TMDB API'

    def handle(self, *args, **kwargs):
        api_key = os.getenv('79313ab3de3abf8b796b2e7e8a890c6b')
        if not api_key:
            self.stdout.write(self.style.ERROR('TMDB_API_KEY not found in environment variables'))
            return

        url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}'
        response = requests.get(url)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f'Error fetching data from TMDB API: {response.status_code}'))
            return

        movies = response.json().get('results', [])
        for movie in movies:
            if not Movie.objects.filter(title=movie['title']).exists():
                Movie.objects.create(
                    title=movie['title'],
                    description=movie['overview'],
                    release_date=movie['release_date'],
                    rating=movie['vote_average'],
                    poster_url=f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                )
        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored movies'))
