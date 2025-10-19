import csv, os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recommender.models import Movie, Rating

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../../data/ml-100k')
MOVIES_FILE = os.path.abspath(os.path.join(DATA_DIR, 'u.item'))
RATINGS_FILE = os.path.abspath(os.path.join(DATA_DIR, 'u.data'))

class Command(BaseCommand):
    help = "Load MovieLens 100k dataset into the database."

    def handle(self, *args, **kwargs):
        self.stdout.write("📦 Loading MovieLens dataset...")

        # 1️⃣ Load Movies
        with open(MOVIES_FILE, encoding='latin-1') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                movie_id, title, release_date, *_ = row
                Movie.objects.get_or_create(
                    id=int(movie_id),
                    defaults={
                        'title': title,
                        'description': f"Released: {release_date or 'Unknown'}",
                        'genre': 'Unknown',  # optional
                        'poster_url': '',     # optional
                    },
                )
        self.stdout.write("✅ Movies loaded.")

        # 2️⃣ Load Users
        user_ids = set()
        with open(RATINGS_FILE, 'r') as f:
            for line in f:
                user_id, movie_id, rating, timestamp = line.strip().split('\t')
                user_ids.add(int(user_id))
        for uid in user_ids:
            User.objects.get_or_create(username=f"user{uid}", defaults={'password': 'pbkdf2_sha256$fake'})

        self.stdout.write(f"✅ Users created: {len(user_ids)}")

        # 3️⃣ Load Ratings
        count = 0
        with open(RATINGS_FILE, 'r') as f:
            for line in f:
                user_id, movie_id, rating, timestamp = line.strip().split('\t')
                try:
                    user = User.objects.get(username=f"user{user_id}")
                    movie = Movie.objects.get(id=int(movie_id))
                    Rating.objects.create(user=user, movie=movie, rating=int(rating))
                    count += 1
                except Exception as e:
                    continue
        self.stdout.write(f"✅ Ratings loaded: {count}")
