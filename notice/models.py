from django.db import models


class Board(models.Model):
    # Board Category
    COMMON, ELTEC, LIBERAL, APPLE, NATURE, MUSIC, ARTNDESIGN, TEACHERS, \
    BIZ, CONVERGENCE, MED, NURSING, PHARM, SCRANTON, HOKMA, OTHER, TEST = range(17)

    BOARD_CATEGORY_CHOICE = [
        (COMMON, "Common"),
        (ELTEC, "Eltec"),
        (LIBERAL, "Liberal"),
        (APPLE, "Apple"),
        (NATURE, "Nature"),
        (MUSIC, "Music"),
        (ARTNDESIGN, "Artndesign"),
        (TEACHERS, "Teachers"),
        (BIZ, "Biz"),
        (CONVERGENCE, "Convergence"),
        (MED, "Med"),
        (NURSING, "Nursing"),
        (PHARM, "Pharm"),
        (SCRANTON, "Scranton"),
        (HOKMA, "Hokma"),
        (OTHER, "Other"),
        (TEST, "Test")
    ]

    # Board Type
    COMMON, CATEGORY, NON_CATEGORY, NON_CATEGORY_NON_WRITER, COMPLEX = range(5)
    BOARD_TYPE_CHOICE = [
        (COMMON, "Common"),
        (CATEGORY, "Category"),
        (NON_CATEGORY, "Non-Category"),
        (NON_CATEGORY_NON_WRITER, "Non-Category&Non-Writer"),
        (COMPLEX, "Complex")
    ]

    board_category = models.IntegerField(choices=BOARD_CATEGORY_CHOICE)
    board_id = models.IntegerField(null=False)
    board_type = models.IntegerField(choices=BOARD_TYPE_CHOICE)
    base_url = models.CharField(max_length=300, null=False)
    next_url = models.CharField(max_length=300, blank=True)
    title = models.CharField(max_length=20, null=False)
    saved_latest = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def update_latest(self, new_latest):
        self.saved_latest = new_latest
        self.save()

    def init(self):
        self.saved_latest = 0
        self.save()


class Notice(models.Model):
    board_category = models.IntegerField(choices=Board.BOARD_CATEGORY_CHOICE, db_index=True)
    board_id = models.IntegerField()
    num = models.IntegerField()
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=5, null=True, blank=True)
    date = models.DateField(auto_now_add=False)
    url = models.CharField(max_length=300)
    push = models.BooleanField(default=False)

    def set_push(self, push=True):
        self.push = push
        self.save()

    def __str__(self):
        return self.title
