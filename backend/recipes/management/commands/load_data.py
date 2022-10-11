import csv
import os

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Loading Ingredients...")

        file_path = os.path.join(
            os.path.abspath(os.path.dirname("manage.py")),
            "recipes/data/ingredients.csv",
        )

        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(
                csvfile, fieldnames=["name", "measurement_unit"]
            )
            for row in reader:
                Ingredient.objects.update_or_create(**row)

        self.stdout.write(self.style.SUCCESS("All Ingredients are loaded."))
