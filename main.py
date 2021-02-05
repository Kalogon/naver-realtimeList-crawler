import json
import datetime
from settings import load_settings, SETTINGS
from realTimeListCrawler import RealTimeListCrawler

if __name__ == "__main__":
    load_settings()
    print(f"Naver real time list crawler v{SETTINGS.version}")
    print("* 설정")
    print(f"* date-range    : {SETTINGS.startTime} ~ {SETTINGS.endTime}")
    print(f"* visit-interval: {SETTINGS.sleep_interval}")
    print(f"[LOG] 크롤링 시작: 날짜 {datetime.datetime.now()}")
    c=RealTimeListCrawler(SETTINGS.startTime, SETTINGS.endTime)
    try:
        c.start()
    except Exception as e:
        print("[ERR] 크롤링 중 오류 발생:", e)