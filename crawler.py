#%%
#crawler

import urllib.request
from urllib import parse
import json
from datetime import datetime
import requests

class Crawler(object):
    
    def __init__(self):
        Crawler.self = self
    
    #기상청 API 활용하여 동네예보 정보 수집 (격자 좌표 사용)
    def fore_weather_fetch(self,xy_dict):
        x = xy_dict['x']
        y = xy_dict['y']
        app_key = "OpDeCpVjBnXyhjQRmnwHAh6z923MxbOZlXnrmVmHE5BHu%2Bl%2BsRGzwIrlwELxIdo26xXh5CwjEPPBAmOf3jX%2FNw%3D%3D"
        
        #- Base_time  : 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300 (1일 8회)
        #- API 제공 시간(~이후) : 02:10, 05:10, 08:10, 11:10, 14:10, 20:10, 23:10
        
        now = datetime.now()
        base_date = now.strftime('%Y%m%d')
        inthour = int(now.strftime('%H%M'))
        
        if (inthour >= 2310) or (inthour < 210):
            base_time = '2300'
        elif 210 <= inthour <510:
            base_time = '0200'
        elif 510 <= inthour <810:
            base_time = '0500'
        elif 810 <= inthour <1110:
            base_time = '0800'
        elif 1110 <= inthour <1410:
            base_time = '1100'
        elif 1410 <= inthour <1710:
            base_time = '1400'
        elif 1710 <= inthour <2000:
            base_time = '1700'
        elif 2000 <= inthour <2300:
            base_time = '2000'
        
        url = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?base_date={}&base_time={}&nx={}&ny={}&numOFRows=30&pageNO=3&ServiceKey={}&_type=json".format(base_date,base_time,x,y, app_key)
        #print(url)
        with urllib.request.urlopen(url) as response:
            self.fore_weather_data = json.loads(response.read().decode("utf-8"))

        return self.fore_weather_data
    
    #기상청 API 활용하여 초단기실황 정보 수집
    def now_weather_fetch(self,xy_dict):
        x = xy_dict['x']
        y = xy_dict['y']
        app_key = "OpDeCpVjBnXyhjQRmnwHAh6z923MxbOZlXnrmVmHE5BHu%2Bl%2BsRGzwIrlwELxIdo26xXh5CwjEPPBAmOf3jX%2FNw%3D%3D"
        now = datetime.now()
        base_date = now.strftime('%Y%m%d')
        
        #초단기실황은 당일의 정보만 호출이 가능한데, 매시 40분에 해당 시각의 정보 호출 가능. 따라서 00:00~00:40 에는 수집 불가.
        if now.strftime('%H') == '00' and int(now.strftime('%M')) < 40 :
            print ('프로그램이 사용 불가능합니다. 12시 40분 이후에 시도해주세요')
            exit()
        elif now.strftime('%H') != '00' and int(now.strftime('%M')) < 40:
            hour = str(int(now.strftime('%H')) - 1)
        else :
            hour = now.strftime('%H')
        
        minute = '00'
        base_time = hour+minute
        url = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastGrib?base_date={}&base_time={}&nx={}&ny={}&ServiceKey={}&_type=json".format(base_date,base_time,x,y, app_key)
        #print(url)
        with urllib.request.urlopen(url) as response:
            self.now_weather_data = json.loads(response.read().decode("utf-8"))

        return self.now_weather_data
    
    # 환경공단 API 활용하여 미세먼지 정보 수집 (tm 좌표 사용)
    def fine_dust_fetch(self,tm_list):
        app_key = "OpDeCpVjBnXyhjQRmnwHAh6z923MxbOZlXnrmVmHE5BHu%2Bl%2BsRGzwIrlwELxIdo26xXh5CwjEPPBAmOf3jX%2FNw%3D%3D"
        tm_x = tm_list[0]
        tm_y= tm_list[1]
        url = "http://openapi.airkorea.or.kr/openapi/services/rest/MsrstnInfoInqireSvc/getNearbyMsrstnList?ServiceKey={}&tmX={}&tmY={}&_returnType=json".format(
            app_key,tm_x,tm_y)
        with urllib.request.urlopen(url) as response:
            hjson = json.loads(response.read().decode("utf-8"))
        station_name = hjson['list'][0]['stationName']
        Url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?stationName={}&dataTerm=DAILY&ServiceKey={}&ver=1.3&_returnType=json".format(
            parse.quote(station_name), app_key)
        #print(Url)

        with urllib.request.urlopen(Url) as response:
            self.fine_dust_data = json.loads(response.read().decode("utf-8"))
        return self.fine_dust_data