# coding=utf-8
import json, requests
from sqlite3 import Timestamp
from datetime import datetime, timedelta 
from ics import Calendar, DisplayAlarm, Event

class Date_Kit:
    def __init__(self) -> None:
        self.now = datetime.now()
        self.next = self.now + timedelta(days=30)
        self.start = self.now.strftime("%Y-%m-%d")
        self.end = self.next.strftime("%Y-%m-%d")
        
        self.start_ts = int(datetime.strptime(self.start, '%Y-%m-%d').timestamp())
        self.end_ts = int(datetime.strptime(self.end, '%Y-%m-%d').timestamp())
        self.now_ts = int(datetime.timestamp(self.now))*1000

dt = Date_Kit()


# def get_time():
#     dt_obj = datetime.now()
#     end_obj = dt_obj + timedelta(days=1)
#     start = dt_obj.strftime("%Y-%m-%d")
#     end = end_obj.strftime("%Y-%m-%d")
#     return start, end

def get_response():
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
    response = requests.get('https://www.jisilu.cn/data/calendar/get_calendar_data/', params=params, headers=headers)
    return json.loads(response.text)

def main():
    c = Calendar()
    for i in get_response():
        if  '申购日' in i.get('title'):
            print(i)
            start_date = datetime.strptime(dt.start, '%Y-%m-%d').date()
            if start_date >= datetime.now().date():
                e = Event()
                e.name  = i.get('title')
                # 9:30 - 11:30
                # e.begin = data['STARTDATE'].replace("T00:00:00", " 01:30:00")  #DTEND:20210415T193000Z
                # e.end   = data['STARTDATE'].replace("T00:00:00", " 03:30:00") 
                e.begin = i.get('start') + ' 01:30:00'
                e.end = i.get('start') + ' 03:30:00'
                e.alarms.append(DisplayAlarm(trigger=timedelta(minutes=30), display_text=e.name)) # 10:00
                c.events.add(e)
           
    with open('kzz.ics', 'w') as my_file:
        my_file.writelines(c)
        
if __name__ == '__main__':
    main()