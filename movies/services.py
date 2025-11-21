import requests
import logging
from django.core.cache import cache
from django.conf import settings
from .models import Movie
from datetime import datetime

logger = logging.getLogger(__name__)

class TMDbService:
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_BASE_URL
        self.timeout = 10

    def _make_request(self, endpoint, params=None):
        """Make API request with error handling"""
        if not self.api_key:
            raise Exception("TMDb API key not configured")
        
        if params is None:
            params = {}
        
        params['api_key'] = self.api_key
        
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"TMDb API error: {str(e)}")
            raise Exception(f"Failed to fetch data from TMDb: {str(e)}")

    def get_trending_movies(self, time_window='week'):
        """Fetch trending movies with caching"""
        cache_key = f"trending_movies_{time_window}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"Returning cached trending movies for {time_window}")
            return cached_data
        
        try:
            data = self._make_request(f"/trending/movie/{time_window}")
            movies_data = data.get('results', [])
            movies = self._process_and_save_movies(movies_data)
            
            # Cache for 1 hour
            cache.set(cache_key, movies, 3600)
            return movies
        except Exception as e:
            logger.error(f"Error fetching trending movies: {str(e)}")
            # Return cached data if available, even if expired
            all_movies = Movie.objects.all().order_by('-popularity')[:20]
            return all_movies

    def get_recommendations(self, movie_id):
        """Fetch movie recommendations with caching"""
        cache_key = f"recommendations_movie_{movie_id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"Returning cached recommendations for movie {movie_id}")
            return cached_data
        
        try:
            data = self._make_request(f"/movie/{movie_id}/recommendations")
            movies_data = data.get('results', [])
            movies = self._process_and_save_movies(movies_data)
            
            cache.set(cache_key, movies, 3600)
            return movies
        except Exception as e:
            logger.error(f"Error fetching recommendations: {str(e)}")
            return []

    def _process_and_save_movies(self, movies_data):
        """Process and save movies to database"""
        movies = []
        for movie_data in movies_data:
            try:
                movie, created = Movie.objects.update_or_create(
                    tmdb_id=movie_data['id'],
                    defaults={
                        'title': movie_data.get('title', ''),
                        'description': movie_data.get('overview', ''),
                        'poster_url': f"https://image.tmdb.org/t/p/w342{movie_data['poster_path']}" if movie_data.get('poster_path') else '',
                        'release_date': movie_data.get('release_date'),
                        'vote_average': movie_data.get('vote_average', 0),
                        'vote_count': movie_data.get('vote_count', 0),
                        'popularity': movie_data.get('popularity', 0),
                    }
                )
                movies.append(movie)
            except Exception as e:
                logger.error(f"Error processing movie {movie_data.get('id')}: {str(e)}")
                continue
        
        return movies
