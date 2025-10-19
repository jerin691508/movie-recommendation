from .ml.hybrid import recommend_for_user
from .serializers import (
    RegisterSerializer, UserSerializer,
    MovieSerializer, RatingSerializer,
    WatchlistSerializer, FeedbackSerializer
)
from .models import Movie, Rating, WatchlistItem, Feedback
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# 1️⃣ User Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# 2️⃣ User Profile
class UserProfileView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# 3️⃣ Movie List
class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]

# 4️⃣ Movie Detail
class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]

# 5️⃣ Rate Movie
class RateMovieView(APIView):
    def post(self, request, pk):
        movie = Movie.objects.get(id=pk)
        rating_value = request.data.get('rating')

        rating, created = Rating.objects.update_or_create(
            user=request.user, movie=movie,
            defaults={'rating': rating_value}
        )

        all_ratings = Rating.objects.filter(movie=movie)
        avg = sum(r.rating for r in all_ratings) / all_ratings.count()
        movie.rating_avg = avg
        movie.save()

        return Response({'message': 'Rating saved', 'avg': avg})

# 6️⃣ Search Movies
class SearchView(APIView):
    def get(self, request):
        query = request.GET.get('query', '')
        movies = Movie.objects.filter(title__icontains=query)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

# 7️⃣ Watchlist
class WatchlistView(APIView):
    def get(self, request):
        items = WatchlistItem.objects.filter(user=request.user)
        serializer = WatchlistSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        movie_id = request.data.get('movie_id')
        movie = Movie.objects.get(id=movie_id)
        WatchlistItem.objects.get_or_create(user=request.user, movie=movie)
        return Response({'message': 'Added to watchlist'})

    def delete(self, request):
        movie_id = request.data.get('movie_id')
        WatchlistItem.objects.filter(user=request.user, movie_id=movie_id).delete()
        return Response({'message': 'Removed from watchlist'})

# 8️⃣ Feedback
class FeedbackView(APIView):
    def post(self, request):
        Feedback.objects.create(user=request.user, message=request.data.get('message'))
        return Response({'message': 'Feedback submitted'})

# 9️⃣ Recommendations
class RecommendationView(APIView):
    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        if user:
            try:
                ids = recommend_for_user(user.id, top_k=20)
                if ids:
                    movies_qs = Movie.objects.filter(id__in=ids)
                    id_to_movie = {m.id: m for m in movies_qs}
                    ordered = [id_to_movie[i] for i in ids if i in id_to_movie]
                    serializer = MovieSerializer(ordered, many=True)
                    return Response(serializer.data)
            except Exception as e:
                print("Recommendation error:", e)

        top_movies = Movie.objects.order_by('-rating_avg')[:20]
        serializer = MovieSerializer(top_movies, many=True)
        return Response(serializer.data)

# 🔟 User History (placeholder)
class UserHistoryView(APIView):
    def get(self, request):
        ratings = Rating.objects.filter(user=request.user)
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)