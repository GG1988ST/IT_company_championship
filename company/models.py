from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    TAB_MAX_LENGTH=128
    name = models.CharField(max_length=TAB_MAX_LENGTH,unique=True)
    #number_of_employee = models.IntegerField(default=0)
    slug=models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Company(models.Model):
    NAME_MAX_LENGTH=128
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_MAX_LENGTH,unique=True)
    location = models.CharField(max_length=NAME_MAX_LENGTH)
    #number_of_employee = models.IntegerField(default=0)
    rates = models.IntegerField(default=0)
    slug1=models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        self.slug1 = slugify(self.name)
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Comments(models.Model):
    COMMENTS_MAX_LENGTH = 400
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    comments = models.CharField(max_length=COMMENTS_MAX_LENGTH)
    date = models.DateField(auto_now=False)
    def __str__(self):
        return self.title
