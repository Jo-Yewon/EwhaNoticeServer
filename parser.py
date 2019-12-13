import requests
from bs4 import BeautifulSoup
import csv
from django.core import serializers

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EwhaNoticeServer.settings")

import django
django.setup()

from common.models import CommonNotice
from eltec.models import EltecNotice


def get_common_notice(file_name="board_data/common_board_list.csv"):
    base_url = 'https://www.ewha.ac.kr/mbs/ewhakr/jsp/board/'
    with open(file_name, 'r', encoding='utf-8') as f:
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
            CommonNotice(boardId=board_id,
                         num=int(td_list[0].string),
                         category=category,
                         title=td_list[2].a.string.strip(),
                         link=base_url + td_list[2].a.attrs['href'],
                         date=td_list[3].string.strip()).save()

    # update latest
    with open(file_name, 'w', encoding='utf-8', newline="") as f:
        writer = csv.writer(f)
        writer.writerow([board_id, url, latest])

    # TODO Send push alarm to FCM
    new_notices_json = serializers.serialize('json', CommonNotice.objects.filter(num__gt=db_latest))


def get_eltec_notice(file_list="board_data/eltec_board_list.csv", file_latest="board_data/eltec_board_latest.csv"):
    base_url = 'http://cms.ewha.ac.kr/user/'
    get_url = 'http://cms.ewha.ac.kr/user/boardList.action?boardId={}'
    with open(file_list, 'r', encoding='utf-8') as f_list:
        with open(file_latest, 'r', encoding='utf-8') as f_latest:
            # get board_list data
            reader_list = list(csv.reader(f_list))
            reader_latest = list(csv.reader(f_latest))
            new_latest_list = []
            for i in range(len(reader_list)):
                board_id, category, db_latest = reader_list[i][0], reader_list[i][1], int(reader_latest[i][0])
                if category == '1':
                    category = True
                else:
                    category = False

                # get data from url
                req = requests.get(get_url.format(board_id))
                req.encoding = 'utf-8'
                html = req.text
                soup = BeautifulSoup(html, 'html.parser')

                # Find first new notice(without special)
                notices = soup.select('tbody > tr')
                for i in range(len(notices)):
                    notice = notices[i]
                    td_list = notice.find_all("td")
                    if td_list is None:
                        continue
                    notice_num = td_list[0].string
                    if notices[i].find_all("td")[0].string is not None:
                        latest = int(notice_num)
                        if latest <= db_latest:
                            return  # No new notice
                        break

                # Get new notices
                for j in range(latest - db_latest):
                    notice = notices[i + j]
                    td_list = notice.find_all("td")
                    if category:
                        EltecNotice(boardId=board_id,
                                    num=int(td_list[0].string),
                                    category=td_list[1].string,
                                    title=td_list[2].text,
                                    link=base_url + td_list[2].a.attrs['href'],
                                    date=td_list[4].text.strip()).save()
                    else:
                        EltecNotice(boardId=board_id,
                                    num=int(td_list[0].string),
                                    title=td_list[1].a.text.strip(),
                                    link=base_url + td_list[1].a.attrs['href'],
                                    date=td_list[3].text.strip()).save()

                # save new latest
                new_latest_list.append(latest)

            # Update new latest
            with open(file_latest, 'w', encoding='utf-8', newline="") as f_latest:
                writer = csv.writer(f_latest)
                for new_latest in new_latest_list:
                    writer.writerow([new_latest])

    # TODO Send push alarm to FCM
    new_notices_json = serializers.serialize('json', EltecNotice.objects.filter(num__gt=db_latest))


get_eltec_notice()
