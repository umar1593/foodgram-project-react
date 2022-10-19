from django.core.management import BaseCommand
from recipes.models import Tag

tags = [
    {'name': 'Завтрак', 'color': '#E26C2D', 'slug': 'zavtrak'},
    {'name': 'Обед', 'color': '#49B64E', 'slug': 'obed'},
    {'name': 'Ужин', 'color': '#8775D2', 'slug': 'yzhin'}
]


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Tag.objects.bulk_create(Tag(**tag) for tag in tags)
        self.stdout.write(self.style.SUCCESS('Теги загружены!'))
