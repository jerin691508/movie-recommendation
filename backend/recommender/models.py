from django.db import models
from django.contrib.auth.models import User

# 1️⃣ User Profile - extends Django user
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username


# 2️⃣ Movie Model
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=100, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    rating_avg = models.FloatField(default=0.0)
    poster_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


# 3️⃣ Rating Model
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField()  # 1.0 - 5.0
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.movie.title}: {self.rating}"


# 4️⃣ Watchlist Model
class WatchlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


# 5️⃣ Feedback Model
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"
