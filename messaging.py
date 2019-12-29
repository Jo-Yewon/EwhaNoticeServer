import firebase_admin
from firebase_admin import credentials, messaging
from notice.models import Board, Notice
from django.core import serializers


def send_push():
    cred = credentials.Certificate("ewhacsenotice2-firebase-adminsdk-48h6h-28711e84e8.json")
    firebase_admin.initialize_app(cred)

    for i in range(len(Board.BOARD_CATEGORY_CHOICE)):
        topic = Board.BOARD_CATEGORY_CHOICE[i][1]
        # new_notices = Notice.objects.filter(board_category=i, push=False)
        new_notices = Notice.objects.filter(board_category=i)
        if len(new_notices) == 0:
            continue

        message = messaging.Message(
            data={
                'data': serializers.serialize('json', new_notices)
            },
            topic=topic,
        )

        response = messaging.send(message)
        print(response)
        for notice in new_notices:
            notice.set_push()
