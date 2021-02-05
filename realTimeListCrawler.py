import json
import requests
from bs4 import BeautifulSoup
from time import sleep
from settings import SETTINGS
import pandas
import csv

class RealTimeListCrawler:
    def __init__(self, startTime, endTime):
        self.url = f"https://datalab.naver.com/keyword/realtimeList.naver"
        self.startTime = startTime
        self.endTime = endTime
        self.log = open('log.txt','w')
        self.f = open(f'{startTime}-{endTime}.csv','w', newline='')
        self.wr = csv.writer(self.f)
        self.wr.writerow(["date", "datetime", "keywords"])

    def formatQuery(self, date, time):
        strDate = str(date)
        strTime = str(time)
        dateQuery = strDate[:4] + "-" + strDate[4:6] + "-" + strDate[6:8]
        if time < 10:
            timeQuery = "T0" + strTime + ":00:00"
        else:
            timeQuery = "T" + strTime + ":00:00"
        return dateQuery + timeQuery
    
    def get_chart(self, date, time):
        datetime = self.formatQuery(date, time)
        getUrl = self.url + "?datetime=" + datetime + "&age=all&groupingLevel=0&marketing=-2&news=-2&entertainment=-2&sports=-2"
        keywords_list = list()
        # print(f"[LOG] 기사에 접근: {getUrl}")
        self.log.write(f"[LOG] 기사에 접근: {getUrl}\n")
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        response = session.get(getUrl, headers=headers)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            keywords = soup.select('#content > div > div.keyword_carousel > div > div.section_lst_area.carousel_area > div.keyword_rank.select_date > div > div > ul > li')
            if len(keywords) > 0:
                for keyword in keywords:
                    keywords_list.append(keyword.select_one('span').get_text())
            else:
                keywords = soup.select('#content > div > div.keyword_carousel > div > div > div:nth-child(1) > div > div > ul > li')
                if len(keywords) > 0:
                    for keyword in keywords:
                        keywords_list.append(keyword.select_one('span').get_text())
                else:
                    keywords = soup.select('#content > div > div.selection_area > div.selection_content > div.field_list > div > div li')
                    for keyword in keywords:
                        keywords_list.append(keyword.select_one('span.item_title').get_text())
        else:
            # print(response.status_code)
            self.log.write(f"[ERR] 네트워크 에러 발생 {response.status_code}\n")

        self.wr.writerow([date, datetime, keywords_list])

    def start(self):
        dt_index = pandas.date_range(start=str(self.startTime), end=str(self.endTime))
        dt_list = dt_index.strftime("%Y%m%d").tolist()
        for date in dt_list:
            for time in range(0, 24):
                SETTINGS.sleep()
                try :
                    self.get_chart(date, time)
                except Exception as e:
                    # print(f"[ERR] {date}일 {time}시간의 차트를 가져오던 중 에러 발생: {e}")
                    self.log.write(f"[ERR] {date}일 {time}시간의 차트를 가져오던 중 에러 발생: {e}\n")
                    SETTINGS.sleep_error()
                    pass

        self.f.close()
        self.log.close()
