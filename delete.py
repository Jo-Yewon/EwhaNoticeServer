# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EwhaNoticeServer.settings")
import django

django.setup()

from crawler import *


def delete_outdated_notice():
    notices = Notice.objects.filter(date__lte=datetime.now() - timedelta(days=60))

    slack = Slacker(get_secret("SLACK_TOKEN"))
    send_msg_to_slack("Delete {} notices.".format(len(notices)), slack)

    notices.delete()


if __name__ == '__main__':
    delete_outdated_notice()
