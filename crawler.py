# -*- coding: utf-8 -*-
import os

import requests
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EwhaNoticeServer.settings")

import django

django.setup()

from notice.models import Board, Notice
from messaging import send_push


def get_first_notice(notices):
    # Find the first numbered notice.
    for i in range(len(notices)):
        notice = notices[i]
        td_list = notice.find_all("td")
        notice_num = td_list[0].string
        if notice_num is not None:
            return i, int(notice_num)
    return -1, -1


def error(board, message):
    print("board id: {}, board title: {}, {}.".format(board.board_id, board.title, message))


def get_notice():
    boards = Board.objects.all()
    for board in boards:
        try:
            if board.board_type == Board.CATEGORY:
                req = requests.get(board.base_url + board.next_url)
                req.encoding = 'utf-8'
                notices = BeautifulSoup(req.text, 'html.parser').select('tbody > tr')[1:]
                if len(notices) == 0:
                    error(board, "cannot crawl")

                latest_index, latest_num = get_first_notice(notices)
                if latest_index == -1 or latest_num <= board.saved_latest:
                    continue

                for notice in notices[latest_index:]:
                    td_list = notice.find_all("td")
                    num = int(td_list[0].string)
                    if num <= board.saved_latest:
                        break
                    Notice(board_category=board.board_category,
                           board_id=board.board_id,
                           num=num,
                           title=td_list[2].text,
                           category=td_list[1].string,
                           date=td_list[4].text.strip(),
                           url=board.base_url + td_list[2].a.attrs['href']).save()

            elif board.board_type == Board.NON_CATEGORY:
                req = requests.get(board.base_url + board.next_url)
                req.encoding = 'utf-8'
                notices = BeautifulSoup(req.text, 'html.parser').select('table > tr')[1:]
                if len(notices) == 0:
                    error(board, "cannot crawl")

                latest_index, latest_num = get_first_notice(notices)
                if latest_index == -1 or latest_num <= board.saved_latest:
                    continue

                for notice in notices[latest_index:]:
                    td_list = notice.find_all("td")
                    num = int(td_list[0].string)
                    if num <= board.saved_latest:
                        break
                    Notice(board_category=board.board_category,
                           board_id=board.board_id,
                           num=num,
                           title=td_list[1].a.text.strip(),
                           category=None,
                           date=td_list[3].text.strip(),
                           url=board.base_url + td_list[1].a.attrs['href']).save()

            elif board.board_type == Board.NON_CATEGORY_NON_WRITER:
                req = requests.get(board.base_url + board.next_url)
                req.encoding = 'utf-8'
                notices = BeautifulSoup(req.text, 'html.parser').select('tbody > tr')[1:]
                if len(notices) == 0:
                    error(board, "cannot crawl")

                latest_index, latest_num = get_first_notice(notices)
                if latest_index == -1 or latest_num <= board.saved_latest:
                    continue

                for notice in notices[latest_index:]:
                    td_list = notice.find_all("td")
                    num = int(td_list[0].string)
                    if num <= board.saved_latest:
                        break
                    Notice(board_category=board.board_category,
                           board_id=board.board_id,
                           num=num,
                           title=td_list[1].a.text.strip(),
                           category=None,
                           date=td_list[2].text.strip(),
                           url=board.base_url + td_list[1].a.attrs['href']).save()

            elif board.board_type == Board.COMPLEX:
                req = requests.get(board.base_url + board.next_url)
                req.encoding = 'utf-8'
                notices_num = BeautifulSoup(req.text, 'html.parser').select('td.no_list')
                notices_title = BeautifulSoup(req.text, 'html.parser').select('td.title_list')
                notices_date = BeautifulSoup(req.text, 'html.parser').select('td.date_list')
                if len(notices_num) == 0:
                    error(board, "cannot crawl")

                for i in range(len(notices_num)):
                    if notices_num[i].text != '':
                        latest_index, latest_num = i, int(notices_num[i].text)
                        break

                for i in range(latest_index, len(notices_num)):
                    num = int(notices_num[i].text)
                    if num <= board.saved_latest:
                        break
                    Notice(board_category=board.board_category,
                           board_id=board.board_id,
                           num=num,
                           title=notices_title[i].text.strip(),
                           category=None,
                           date=notices_date[i].text.strip(),
                           url=board.base_url + notices_title[i].a.attrs['href']).save()

            # 3. update latest
            board.update_latest(latest_num)

        except:
            print("Error occurred in crawling", board.id)


if __name__ == '__main__':
    get_notice()
    send_push()
