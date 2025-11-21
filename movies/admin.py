from django.contrib import admin
from .models import Movie, Favorite

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'tmdb_id', 'popularity', 'vote_average', 'created_at']
    list_filter = ['created_at', 'vote_average']
    search_fields = ['title', 'tmdb_id']
    readonly_fields = ['tmdb_id', 'created_at', 'updated_at']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'movie__title']
