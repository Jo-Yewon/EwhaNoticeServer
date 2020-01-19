import firebase_admin
from firebase_admin import credentials, messaging
from notice.models import Board, Notice


def send_push():
    cred = credentials.Certificate("./ewhanotice-firebase-adminsdk-sgf5x-dd0dcd357b.json")
    firebase_admin.initialize_app(cred)

    for i in range(len(Board.BOARD_CATEGORY_CHOICE)):
        topic = Board.BOARD_CATEGORY_CHOICE[i][1]
        new_notices = Notice.objects.filter(board_category=i, push=False)
        if len(new_notices) == 0:
            continue
        elif len(new_notices) > 50:
            new_notices = new_notices[:50]

        data = {}
        for j in range(len(new_notices)):
            notice = new_notices[j]
            data[str(j)] = str(notice.board_id) + '&' + notice.title

        message = messaging.Message(
            data=data,
            topic=topic
        )

        messaging.send(message)

        for notice in new_notices:
            notice.set_push()
