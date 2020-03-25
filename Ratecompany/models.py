from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)
        
# Create your models here.
class Category(models.Model):
    TAB_MAX_LENGTH = 128
    name = models.CharField(max_length=TAB_MAX_LENGTH, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = 'Categories'


class Company(models.Model):
    NAME_MAX_LENGTH = 128
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    image = models.ImageField(max_length=1000, upload_to='img', default='img/baidu.png', blank=True)
    location = models.CharField(max_length=NAME_MAX_LENGTH)
    salary=IntegerRangeField(min_value=1, max_value=5)
    wellfare=IntegerRangeField(min_value=1, max_value=5)
    atmosphere=IntegerRangeField(min_value=1, max_value=5)
    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class Comments(models.Model):
    COMMENTS_MAX_LENGTH = 400
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='comments')
    comments = models.CharField(max_length=COMMENTS_MAX_LENGTH)
    date = models.DateField(auto_now=False, null=True)
    classify = models.IntegerField(choices=((0, 'salary'), (1, 'wellfare'), (2, 'atmosphere')))
    score = models.IntegerField(verbose_name="mark")
    user_name = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Comments'

class UserProfile(AbstractUser):
  
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users', null=True)
    sex = models.IntegerField(verbose_name="gender", choices=((0, 'male'), (1, 'female')), default=0)
    phone = models.CharField(verbose_name="telephone number", null=True, max_length=11)
    address = models.CharField(verbose_name="address", null=True, max_length=255)
    image = models.ImageField(max_length=1000, upload_to='avatar', verbose_name='img', blank=True,
                              default='avatar/default.jpg')
