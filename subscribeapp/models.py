from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from projectapp.models import Project


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             # 장고에서 기본으로 지원해주는 User
                             related_name='subscription', null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name='subscription', null=False)

    class Meta:  # 외부설정정보 지정
        unique_together = ['user', 'project']


