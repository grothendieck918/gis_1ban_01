from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Article(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL,
                               related_name='article', null=True)
    # 이 유저 객체가 없어졌을때 남아있는 article객체는 어떻게할것인가 사라지지는않지만 작성지가안보임
    
    title = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='article/', null=True)
    # article폴더가생겨서 그안에 게시글관련 사진이저장됨
    content = models.TextField(null=True)
    # 긴 텍스트를 받을때 TextField
    
    created_at = models.DateField(auto_now_add=True, null=True)
    # 이 객체가 생성되는순간에 현재시간이 저장됨