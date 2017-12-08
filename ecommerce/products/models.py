from django.db import models
from taggit.managers import TaggableManager 
from django.db.models.signals import pre_save, post_save
from django.urls import reverse 
from django.db.models import Q

from .utils import unique_slug_generator

class ProductQuerySet(models.query.QuerySet):
    def available(self):
        return self.filter(available=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self,query):
        lookups = (Q(name__icontains=query)|
                   Q(description__icontains=query)|
                   Q(price__icontains=query)|
                   Q(tags__name__icontains=query))
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().available()

    def available(self): #Product.objects.featured() 
        return self.get_queryset().available()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self,query):
        return self.get_queryset().available().search(query)





class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def __str__(self):
        return self.name

    

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    tags = TaggableManager()
    objects = ProductManager()

    def get_absolute_url(self):
        return reverse("products:detail",kwargs={"slug":self.slug})

    

    def __str__(self):
        return self.name
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)