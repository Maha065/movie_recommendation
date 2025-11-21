from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Movie, Favorite
from .serializers import MovieSerializer, UserRegistrationSerializer, FavoriteSerializer
from .services import TMDbService
import logging

logger = logging.getLogger(__name__)

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def trending(self, request):
        """Get trending movies"""
        try:
            tmdb_service = TMDbService()
            time_window = request.query_params.get('time_window', 'week')
            movies = tmdb_service.get_trending_movies(time_window)
            serializer = self.get_serializer(movies, many=True, context={'request': request})
            return Response({
                'status': 'success',
                'count': len(serializer.data),
                'results': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in trending endpoint: {str(e)}")
            return Response(
                {'status': 'error', 'message': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def recommended(self, request, pk=None):
        """Get recommendations for a specific movie"""
        try:
            tmdb_service = TMDbService()
            recommendations = tmdb_service.get_recommendations(pk)
            serializer = self.get_serializer(recommendations, many=True, context={'request': request})
            return Response({
                'status': 'success',
                'count': len(serializer.data),
                'results': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in recommendations endpoint: {str(e)}")
            return Response(
                {'status': 'error', 'message': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    @action(detail=False, methods=['post', 'get'], permission_classes=[IsAuthenticated])
    def favorites(self, request):
        """Add or retrieve favorite movies"""
        if request.method == 'POST':
            serializer = FavoriteSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        favorites = Favorite.objects.filter(user=request.user).select_related('movie')
        serializer = FavoriteSerializer(favorites, many=True, context={'request': request})
        return Response({
            'status': 'success',
            'count': len(serializer.data),
            'results': serializer.data
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_favorite(self, request):
        """Remove a movie from favorites"""
        movie_id = request.data.get('movie_id')
        if not movie_id:
            return Response(
                {'error': 'movie_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            favorite = Favorite.objects.get(user=request.user, movie_id=movie_id)
            favorite.delete()
            return Response({'status': 'success', 'message': 'Removed from favorites'})
        except Favorite.DoesNotExist:
            return Response(
                {'error': 'Favorite not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Register a new user"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Logout user (token invalidation handled by client)"""
        return Response({
            'status': 'success',
            'message': 'Logged out successfully'
        })
