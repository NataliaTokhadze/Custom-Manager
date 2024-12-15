from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import Min, Max, Avg, Count
class CategoryManager(models.Manager):
    def with_item_count(self, *args, **kwargs):
        return self.annotate(item_count=Count('items'))

class ItemManager(models.Manager):
    def with_tag_count(self, *args, **kwargs):
        return self.annotate(tag_count=Count('tags'))
class TagManager(models.Manager):
    def popular_tags(self, min_items):
        item_count = self.annotate(item_count=Count('items'))
        return item_count.filter(item_count__gte=min_items)
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    images = GenericRelation('Image', related_query_name="category")
    categories = CategoryManager()

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    images = GenericRelation("Image", related_query_name="item")
    items = ItemManager()

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    items = models.ManyToManyField(Item, related_name='tags', blank=True)
    tags = TagManager()
    def __str__(self):
        return self.name

class Image(models.Model):
    url = models.URLField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')