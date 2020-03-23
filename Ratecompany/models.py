from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser


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


class Company(models.Model):
    NAME_MAX_LENGTH = 128
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    image = models.ImageField(max_length=1000, upload_to='img', default='img/baidu.png', blank=True)
    location = models.CharField(max_length=NAME_MAX_LENGTH)
    salary = models.IntegerField(default=0)
    wellfare = models.IntegerField(default=0)
    atmosphere = models.IntegerField(default=0)


    def __str__(self):
        return self.name


class Comments(models.Model):
    COMMENTS_MAX_LENGTH = 400
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='comments')
    comments = models.CharField(max_length=COMMENTS_MAX_LENGTH)
    date = models.DateField(auto_now=False, null=True)
    classify = models.IntegerField(choices=((0, 'salary'), (1, 'wellfare'), (2, 'atmosphere')))
    score = models.IntegerField(verbose_name="分数")
    user_name = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)


class UserProfile(AbstractUser):
    '''扩展Django自带的User模型'''
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users', null=True)
    sex = models.IntegerField(verbose_name="性别", choices=((0, '男'), (1, '女')), default=0)
    phone = models.CharField(verbose_name="手机号", null=True, max_length=11)
    address = models.CharField(verbose_name="地址", null=True, max_length=255)
    image = models.ImageField(max_length=1000, upload_to='avatar', verbose_name=u'头像', blank=True,
                              default='avatar/default.jpg')