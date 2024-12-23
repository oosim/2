from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class RealTimeTomatoData(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    temperature = models.FloatField()
    humidity = models.FloatField()

    def __str__(self):
        return f"{self.timestamp} - Temp: {self.temperature}, Humidity: {self.humidity}"


# 작기 종료 후 일일 평균 데이터 모델
class DailyTomatoData(models.Model):
    date = models.DateField()
    daytime_avg_temp = models.FloatField()
    nighttime_avg_temp = models.FloatField()
    daytime_avg_humidity = models.FloatField()
    nighttime_avg_humidity = models.FloatField()
    daily_total_light = models.FloatField()

    def __str__(self):
        return f"{self.date} - Day Temp: {self.daytime_avg_temp}, Night Temp: {self.nighttime_avg_temp}"

# 🟢 게시물 모델 (Post)
class TomatoPost(models.Model):
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/tag/{self.slug}/'

class Region(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=50)

    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)

    slug = models.SlugField(max_length=200, allow_unicode=True, null=True, blank=True)
    farm_owner = models.TextField(max_length=100, blank=True)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'| {self.pk} | {self.title} - {self.author}'

class Farm(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farm')
    farm = models.CharField(max_length=100, blank=True)  # 농가 이름
    farm_slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, blank=True, null=True)
    farm_owner = models.CharField(max_length=100, blank=True, null=True) # 농부 이름
    owner_image = models.ImageField(upload_to='farm/images/%Y/%m/%d/', blank=True)
    location = models.CharField(max_length=200, blank=True)  # 농가 위치
    description = models.TextField(blank=True)  # 농가 설명
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.farm}] {self.farm_owner} 농부'

class Recipe(models.Model):
    title = models.CharField(max_length=200)  # 레시피 제목
    description = models.TextField()  # 레시피 설명
    ingredients = models.TextField(null=True, blank=True)  # 🆕 재료 항목
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)  # 이미지 (선택사항)
    crop = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='recipes')  # Post와 연결
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일

    def __str__(self):
        return self.title