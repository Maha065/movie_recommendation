from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie, Favorite

# Serializer for Movie model
class MovieSerializer(serializers.ModelSerializer):
    # Check if current user has favorited this movie
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'tmdb_id', 'title', 'description', 'poster_url', 
                  'release_date', 'vote_average', 'vote_count', 'popularity', 'is_favorite']

    def get_is_favorite(self, obj):
        # Check if request user has favorited this movie
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, movie=obj).exists()
        return False


# Serializer for user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        # Check if passwords match
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        # Create user with hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# Serializer for Favorites
class FavoriteSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)  # Show full movie data
    movie_id = serializers.IntegerField(write_only=True)  # Accept movie_id for input

    class Meta:
        model = Favorite
        fields = ['id', 'movie', 'movie_id', 'added_at']

    def create(self, validated_data):
        movie_id = validated_data.pop('movie_id')
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise serializers.ValidationError("Movie not found")
        
        return Favorite.objects.create(movie=movie, **validated_data)
