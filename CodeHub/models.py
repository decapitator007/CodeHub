from django.conf import settings
from django.db import models
class Question(models.Model):
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content=models.TextField()
    added_time=models.DateTimeField()
class Answer(models.Model):
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content=models.TextField()
    link_to_ques=models.ForeignKey(Question,on_delete=models.CASCADE)
    added_time=models.DateTimeField()
class cfid(models.Model):
    username=models.CharField(max_length=100)
    cfusername=models.CharField(max_length=100)
