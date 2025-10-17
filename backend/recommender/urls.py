from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('movies/', views.MovieListView.as_view(), name='movies'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('movie/<int:id>/rate/', views.rate_movie, name='rate-movie'),

    path('recommendations/', views.get_recommendations, name='recommendations'),
    path('search/', views.search_movies, name='search'),

    path('user/watchlist/', views.get_watchlist, name='get-watchlist'),
    path('user/watchlist/add/<int:id>/', views.add_to_watchlist, name='add-watchlist'),
    path('user/watchlist/remove/<int:id>/', views.remove_from_watchlist, name='remove-watchlist'),

    path('feedback/', views.send_feedback, name='feedback'),
]
