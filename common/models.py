from django.db import models


class Notice(models.Model):
    boardId = models.IntegerField(primary_key=True)
    num = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=False)
    link = models.CharField(max_length=300)
