from django.db import models


class Notice(models.Model):
    boardId = models.IntegerField()
    num = models.IntegerField()
    category = models.CharField(max_length=5)
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=False)
    link = models.CharField(max_length=300)

    def __str__(self):
        return [self.id, self.title]
