from django.core.management.base import BaseCommand
from news.models import PostCategory, Post


class Command(BaseCommand):
    help = 'Удалить все статьи в категории'

    def add_arguments(self, parser):
        parser.add_argument('categories', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["categories"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return

        try:
            category = options['categories']
            posts_in_category = Post.objects.filter(categories__name=category)
            count = posts_in_category.count()
            posts_in_category.delete()
            self.stdout.write(self.style.SUCCESS(
                f'Succesfully deleted {count} news from category {category}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category'))
