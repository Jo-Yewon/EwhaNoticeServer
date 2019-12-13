import requests
from bs4 import BeautifulSoup
import csv
from django.core import serializers

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EwhaNoticeServer.settings")

import django
django.setup()

from common.models import Notice


def get_common_notice(file_name="common_board_list.csv"):
    base_url = 'https://www.ewha.ac.kr/mbs/ewhakr/jsp/board/'
    with open(os.path.dirname(os.path.abspath(__file__)) + '\\' + file_name,
              'r', encoding='utf-8') as f:
        # get board_list data
        reader = csv.reader(f)
        for line in reader:
            board_id, url, db_latest = line[0], base_url + line[1], int(line[2])

    # get data from url
    req = requests.get(url)
    req.encoding = 'utf-8'
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    # Find first new notice(without special)
    notices = soup.select('tbody > tr')
    for i in range(len(notices)):
        notice = notices[i]
        td_list = notice.find_all("td")
        notice_num = td_list[0].string
        if notice_num is not None:
            latest = int(notice_num)
            if latest <= db_latest:
                return  # No new notice
            break

    # Get new notices
    for j in range(latest - db_latest):
        notice = notices[i + j]
        td_list = notice.find_all("td")
        category = td_list[1].string.strip()
        if category != '입학' and category != '등록금' and category != '입찰':
            Notice(boardId=board_id,
                   num=int(td_list[0].string),
                   category=category,
                   title=td_list[2].a.string.strip(),
                   link=base_url + td_list[2].a.attrs['href'],
                   date=td_list[3].string.strip()).save()

    # TODO Send push alarm to FCM
    new_notices_json = serializers.serialize('json', Notice.objects.filter(num__gt=db_latest))

    # update latest
    with open(os.path.dirname(os.path.abspath(__file__)) + '\\' + file_name,
              'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([board_id, url, latest])


get_common_notice()
