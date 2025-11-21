# Movie Recommendation API

A production-ready Django REST Framework API for movie recommendations with:
- TMDb API integration
- JWT Authentication
- Redis caching
- PostgreSQL database
- Docker support
- Comprehensive API documentation

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- Redis 6+
- Docker & Docker Compose (optional)

### Installation

1. Clone repository
\`\`\`bash
git clone https://github.com/yourusername/movie-recommendation-api.git
cd movie-recommendation-api
\`\`\`

2. Create virtual environment
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
\`\`\`

3. Install dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Setup environment
\`\`\`bash
cp .env.example .env
# Edit .env with your configuration
\`\`\`

5. Run migrations
\`\`\`bash
python manage.py migrate
\`\`\`

6. Start server
\`\`\`bash
python manage.py runserver
\`\`\`

API available at: http://localhost:8000/api/docs/

## Features

- **Trending Movies** - Get trending movies from TMDb
- **Recommendations** - Get personalized recommendations
- **Favorites** - Save and manage favorite movies
- **Authentication** - Secure JWT-based authentication
- **Caching** - Redis caching for performance
- **API Documentation** - Interactive Swagger UI

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/token/` - Get access token
- `POST /api/auth/token/refresh/` - Refresh access token

### Movies
- `GET /api/movies/trending/` - Get trending movies
- `GET /api/movies/{id}/recommended/` - Get recommendations
- `POST /api/movies/favorites/` - Add to favorites
- `GET /api/movies/favorites/` - Get user's favorites
- `POST /api/movies/remove_favorite/` - Remove from favorites

## Documentation

See the [docs/](docs/) folder for detailed documentation:
- [Installation Guide](docs/INSTALLATION.md)
- [API Documentation](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Testing](docs/TESTING.md)
- [Deployment](docs/DEPLOYMENT.md)

## Development

### Running Tests
\`\`\`bash
pytest
pytest --cov=movies  # With coverage
\`\`\`

### Code Quality
\`\`\`bash
black .
flake8 .
isort .
\`\`\`

### Docker
\`\`\`bash
docker-compose up
\`\`\`

## Environment Variables

See `.env.example` for all available environment variables.

Key variables:
- `DEBUG` - Enable/disable debug mode
- `SECRET_KEY` - Django secret key
- `TMDB_API_KEY` - TMDb API key
- `DATABASE_URL` - Database connection string
- `REDIS_URL` - Redis connection string

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
1. Check existing [Issues](https://github.com/yourusername/movie-recommendation-api/issues)
2. Create a new issue with detailed information
3. Join our [Discussions](https://github.com/yourusername/movie-recommendation-api/discussions)

## Acknowledgments

- [TMDb](https://www.themoviedb.org/) for movie data
- [Django REST Framework](https://www.django-rest-framework.org/)
- [DRF Spectacular](https://drf-spectacular.readthedocs.io/)
