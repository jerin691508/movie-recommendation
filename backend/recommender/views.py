from .ml.hybrid import recommend_for_user
from .serializers import MovieSerializer
from .models import Movie
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Movie, Rating, WatchlistItem, Feedback
from .serializers import (
    RegisterSerializer, UserSerializer,
    MovieSerializer, RatingSerializer,
    WatchlistSerializer, FeedbackSerializer
)

# 1️⃣ User Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# 2️⃣ User Login - returns JWT
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    from django.contrib.auth import authenticate
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# 3️⃣ User Logout
@api_view(['POST'])
def logout_view(request):
    return Response({'message': 'Logout successful'})


# 4️⃣ Get All Movies
class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]


# 5️⃣ Get Single Movie
class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]


# 6️⃣ Rate a Movie
@api_view(['POST'])
def rate_movie(request, id):
    movie = Movie.objects.get(id=id)
    rating_value = request.data.get('rating')

    rating, created = Rating.objects.update_or_create(
        user=request.user, movie=movie,
        defaults={'rating': rating_value}
    )

    # Update average rating
    all_ratings = Rating.objects.filter(movie=movie)
    avg = sum(r.rating for r in all_ratings) / all_ratings.count()
    movie.rating_avg = avg
    movie.save()

    return Response({'message': 'Rating saved', 'avg': avg})


# 7️⃣ Search Movies
@api_view(['GET'])
def search_movies(request):
    query = request.GET.get('query', '')
    movies = Movie.objects.filter(title__icontains=query)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


# 8️⃣ Watchlist Endpoints
@api_view(['GET'])
def get_watchlist(request):
    items = WatchlistItem.objects.filter(user=request.user)
    serializer = WatchlistSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_to_watchlist(request, id):
    movie = Movie.objects.get(id=id)
    item, created = WatchlistItem.objects.get_or_create(user=request.user, movie=movie)
    return Response({'message': 'Added to watchlist'})


@api_view(['DELETE'])
def remove_from_watchlist(request, id):
    WatchlistItem.objects.filter(user=request.user, movie_id=id).delete()
    return Response({'message': 'Removed from watchlist'})


# 9️⃣ Feedback
@api_view(['POST'])
def send_feedback(request):
    Feedback.objects.create(user=request.user, message=request.data.get('message'))
    return Response({'message': 'Feedback submitted'})


# 🔟 Recommendation Placeholder (we’ll implement ML later)

@api_view(['GET'])
def get_recommendations(request):
    """
    Use hybrid recommender to return personalized recommendations.
    If user not authenticated, return top-rated movies as fallback.
    """
    user = request.user if request.user.is_authenticated else None
    if user:
        try:
            ids = recommend_for_user(user.id, top_k=20)
            if ids:
                movies_qs = Movie.objects.filter(id__in=ids)
                # preserve ordering
                id_to_movie = {m.id: m for m in movies_qs}
                ordered = [id_to_movie[i] for i in ids if i in id_to_movie]
                serializer = MovieSerializer(ordered, many=True)
                return Response(serializer.data)
        except Exception as e:
            # gracefully fall back
            print("Recommendation error:", e)

    # fallback: top rated
    top_movies = Movie.objects.order_by('-rating_avg')[:20]
    serializer = MovieSerializer(top_movies, many=True)
    return Response(serializer.data)
