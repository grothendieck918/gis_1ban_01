from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
    # user에 1:1로 연결(연결시켜줄클래스, 연결되어있는User객체가사라지면어떻게될지 정책
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')

    image = models.ImageField(upload_to='profile/', null=True)
    nickname = models.CharField(max_length=30, unique=True)
    message = models.CharField(max_length=200, null=True)