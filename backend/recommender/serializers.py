from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Movie, Rating, WatchlistItem, Feedback

# 1️⃣ User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# 2️⃣ Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user)
        return user


# 3️⃣ Movie Serializer
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


# 4️⃣ Rating Serializer
class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'


# 5️⃣ Watchlist Serializer
class WatchlistSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = WatchlistItem
        fields = '__all__'


# 6️⃣ Feedback Serializer
class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'
