from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Auth
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User
    path('user/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('user/history/', views.UserHistoryView.as_view(), name='user-history'),

    # Movies
    path('movies/', views.MovieListView.as_view(), name='movie-list'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('movie/<int:pk>/rate/', views.RateMovieView.as_view(), name='rate-movie'),
    path('search/', views.SearchView.as_view(), name='search'),

    # Watchlist
    path('user/watchlist/', views.WatchlistView.as_view(), name='user-watchlist'),

    # Feedback
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),

    # Recommendations
    path('recommendations/', views.RecommendationView.as_view(), name='recommendations'),
]