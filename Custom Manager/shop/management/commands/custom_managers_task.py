from django.core.management.base import BaseCommand
from shop.models import Category, Item, Tag
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print(Category.categories.with_item_count())
        print(Item.items.with_tag_count())
        print(Tag.tags.popular_tags(5))