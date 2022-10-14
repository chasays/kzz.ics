import json
from datetime import datetime, timedelta
import requests
from ics import Calendar, DisplayAlarm, Event


class DateKit:
    def __init__(self) -> None:
        self.now = datetime.now()
        self.next = self.now + timedelta(days=30)
        self.start = self.now.strftime("%Y-%m-%d")
        self.end = self.next.strftime("%Y-%m-%d")

        self.start_ts = int(datetime.strptime(
            self.start, '%Y-%m-%d').timestamp())
        self.end_ts = int(datetime.strptime(self.end, '%Y-%m-%d').timestamp())
        self.now_ts = int(datetime.timestamp(self.now))*1000


dt = DateKit()


def get_response():
    """
    return kezhuanzhai response
    """
    headers = {
        'authority': 'www.jisilu.cn',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        'if-modified-since': 'Thu, 13 Oct 2022 02:03:29 GMT',
        'sec-ch-ua': '"Microsoft Edge";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53',
    }

    params = {
        'qtype': 'CNV',
        'start': f'{dt.start_ts}',
        'end': f'{dt.end_ts}',
        '_': f'{dt.now_ts}',
    }
    response = requests.get(
        'https://www.jisilu.cn/data/calendar/get_calendar_data/', params=params, headers=headers)
    return json.loads(response.text)


def main():
    """
    Generate ics file
    """
    c_ins = Calendar()
    for i in get_response():
        if '申购日' in i.get('title'):
            print(i)
            start_date = datetime.strptime(dt.start, '%Y-%m-%d').date()
            if start_date >= datetime.now().date():
                evt = Event()
                evt.name = i.get('title')
                # 9:30 - 11:30
                evt.begin = i.get('start') + ' 01:30:00'
                evt.end = i.get('start') + ' 05:30:00'
                evt.alarms.append(DisplayAlarm(trigger=timedelta(
                    minutes=30), display_text=evt.name))  # 10:00
                c_ins.events.add(evt)

    with open('kzz.ics', 'w',encoding='utf-8') as my_file:
        my_file.writelines(c_ins.serialize())


if __name__ == '__main__':
    main()
