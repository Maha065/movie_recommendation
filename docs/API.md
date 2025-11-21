# API Documentation

## Authentication Endpoints

### Register
\`POST /api/auth/register/\`

Request:
\`\`\`json
{
  "username": "user",
  "email": "user@example.com",
  "password": "Pass123",
  "password_confirm": "Pass123"
}
\`\`\`

Response (201):
\`\`\`json
{
  "status": "success",
  "user": {"id": 1, "username": "user"},
  "tokens": {"access": "...", "refresh": "..."}
}
\`\`\`

### Get Token
\`POST /api/auth/token/\`

### Refresh Token
\`POST /api/auth/token/refresh/\`

## Movie Endpoints

### Trending
\`GET /api/movies/trending/?time_window=week\`

### Recommendations
\`GET /api/movies/{id}/recommended/\`

### Favorites
\`POST /api/movies/favorites/\` - Add
\`GET /api/movies/favorites/\` - Get all
\`POST /api/movies/remove_favorite/\` - Remove
