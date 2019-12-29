from django.db import models


class Board(models.Model):
    # Board Category
    COMMON, ELTEC = range(2)
    BOARD_CATEGORY_CHOICE = [
        (COMMON, "Common"),
        (ELTEC, "Eltec"),
    ]

    # Board Type
    COMMON, CATEGORY, NON_CATEGORY = range(3)
    BOARD_TYPE_CHOICE = [
        (COMMON, "Common"),
        (CATEGORY, "Category"),
        (NON_CATEGORY, "Non-Category")
    ]

    board_category = models.IntegerField(choices=BOARD_CATEGORY_CHOICE)
    board_id = models.IntegerField(null=False)
    board_type = models.IntegerField(choices=BOARD_TYPE_CHOICE)
    base_url = models.CharField(max_length=300, null=False)
    next_url = models.CharField(max_length=300, null=False)
    title = models.CharField(max_length=20, null=False)
    saved_latest = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def update_latest(self, new_latest):
        self.saved_latest = new_latest
        self.save()


class Notice(models.Model):
    board_category = models.IntegerField(choices=Board.BOARD_CATEGORY_CHOICE, db_index=True)
    board_id = models.IntegerField()

    num = models.IntegerField()
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=5, null=True)
    date = models.DateField(auto_now_add=False)
    url = models.CharField(max_length=300)
    push = models.BooleanField(default=False)

    def set_push(self, push=True):
        self.push = push
        self.save()

    def __str__(self):
        return self.title
