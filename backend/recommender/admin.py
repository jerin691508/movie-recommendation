from django.contrib import admin
from .models import UserProfile, Movie, Rating, WatchlistItem, Feedback

admin.site.register(UserProfile)
admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(WatchlistItem)
admin.site.register(Feedback)
