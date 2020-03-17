# -*- coding: utf-8 -*-
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EwhaNoticeServer.settings")

import django

django.setup()

from crawler import *

if __name__ == '__main__':
    try:
        for board in Board.objects.all():
            board.init()
        for notice in Notice.objects.all():
            notice.delete()

        slack = Slacker(get_secret("SLACK_TOKEN"))
        get_notice(slack)

        for notice in Notice.objects.all():
            notice.set_push()

        send_msg_to_slack("Execute reset.py {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), slack)
    except:
        send_msg_to_slack("Error on reset.py {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), slack)
