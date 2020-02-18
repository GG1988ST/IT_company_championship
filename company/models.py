from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    NAME_MAX_LENGTH=128
    name = models.CharField(max_length=NAME_MAX_LENGTH,unique=True)
    location = models.CharField(max_length=NAME_MAX_LENGTH)
    #number_of_employee = models.IntegerField(default=0)
    rates = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug= models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Comments(models.Model):
    USERNAME_MAX_LENGTH = 128
    COMMENTS_MAX_LENGTH = 400
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    upload_by = models.CharField(max_length=USERNAME_MAX_LENGTH,unique=True)
    comments = models.CharField(max_length=COMMENTS_MAX_LENGTH)
    date = models.DateField(auto_now=False)
    def __str__(self):
        return self.title
