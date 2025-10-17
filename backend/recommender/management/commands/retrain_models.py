# backend/recommender/management/commands/retrain_models.py
from django.core.management.base import BaseCommand
from recommender.ml.train import run_training

class Command(BaseCommand):
    help = 'Retrain recommendation models (content & collaborative)'

    def add_arguments(self, parser):
        parser.add_argument('--k', type=int, default=50, help='Number of SVD latent factors')

    def handle(self, *args, **options):
        k = options.get('k', 50)
        self.stdout.write(self.style.NOTICE(f"Retraining models with k={k}"))
        run_training(k_svd=k)
        self.stdout.write(self.style.SUCCESS("Retraining complete"))
