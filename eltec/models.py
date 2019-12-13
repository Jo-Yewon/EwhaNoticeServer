from django.db import models


class EltecNotice(models.Model):
    boardId = models.IntegerField()
    num = models.IntegerField()
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=5, null=True)
    date = models.DateField(auto_now_add=False)
    link = models.CharField(max_length=300)

    def __str__(self):
        return self.title
