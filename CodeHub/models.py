from django.conf import settings
from django.db import models
from ckeditor.fields import RichTextField
class Question(models.Model):
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content=models.TextField()
    added_time=models.DateTimeField()
class Answer(models.Model):
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content=RichTextField()
    link_to_ques=models.ForeignKey(Question,on_delete=models.CASCADE)
    added_time=models.DateTimeField()
class cfid(models.Model):
    username=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    cfusername=models.CharField(max_length=100)
    no_of_q=models.IntegerField(default=0)
    no_of_a=models.IntegerField(default=0)
