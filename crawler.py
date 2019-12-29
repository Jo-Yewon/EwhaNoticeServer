import os

import requests
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EwhaNoticeServer.settings")

import django

django.setup()

from notice.models import Board, Notice
from messaging import send_push


def get_notices_data(url):
    req = requests.get(url)
    req.encoding = 'utf-8'
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup.select('tbody > tr')


def get_first_notice(notices):
    for i in range(len(notices)):
        notice = notices[i]
        td_list = notice.find_all("td")
        notice_num = td_list[0].string
        if notice_num is not None:
            return i, int(notice_num)
    return -1, -1


def get_notice():
    boards = Board.objects.all()
    for board in boards:
        # 1. get data from url
        notices = get_notices_data(board.base_url + board.next_url)
        latest_index, latest_num = get_first_notice(notices)
        if latest_index == -1 or latest_index <= board.saved_latest:
            continue

        # 2. save new notices
        if board.board_type == Board.COMMON:
            for notice in notices[latest_index:]:
                td_list = notice.find_all("td")
                category = td_list[1].string.strip()
                num = int(td_list[0].string)
                if num <= board.saved_latest:
                    break
                if category != '입학' and category != '등록금' and category != '입찰':
                    Notice(board_category=board.board_category,
                           board_id=board.board_id,
                           num=num,
                           title=td_list[2].a.string.strip(),
                           category=category,
                           date=td_list[3].string.strip(),
                           url=board.base_url + td_list[2].a.attrs['href']).save()

        elif board.board_type == Board.CATEGORY:
            for notice in notices[latest_index:]:
                td_list = notice.find_all("td")
                num = int(td_list[0].string)
                Notice(board_category=board.board_category,
                       board_id=board.board_id,
                       num=num,
                       title=td_list[2].text,
                       category=td_list[1].string,
                       date=td_list[4].text.strip(),
                       url=board.base_url + td_list[2].a.attrs['href']).save()

        elif board.board_type == Board.NON_CATEGORY:
            for notice in notices[latest_index:]:
                td_list = notice.find_all("td")
                num = int(td_list[0].string)
                Notice(board_category=board.board_category,
                       board_id=board.board_id,
                       num=num,
                       title=td_list[1].a.text.strip(),
                       category=None,
                       date=td_list[3].text.strip(),
                       url=board.base_url + td_list[1].a.attrs['href']).save()

        # 3. update latest
        board.update_latest(latest_num)


if __name__ == '__main__':
    # get_notice()
    send_push()
