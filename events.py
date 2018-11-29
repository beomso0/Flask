#%%
#events

import json
from datetime import datetime

class Events(object):

    NOW_WEATHER   = 1
    FORE_WEATHER = 2
    FINE_DUST = 3

    def __init__(self, data, event_type):
        self.data = data
        self.event_type = event_type
      
    def process_events(self):
        try : 
            if self.event_type == self.NOW_WEATHER:
                self.temp = self.data['response']['body']['items']['item'][3]['obsrValue']
                self.humidity = self.data['response']['body']['items']['item'][1]['obsrValue']
                self.rain = self.data['response']['body']['items']['item'][0]['obsrValue']
                #rain value : 없음(0), 비(1), 진눈개비(2), 눈(3)
                
            if self.event_type == self.FORE_WEATHER:
                self.sky = self.data['response']['body']['items']['item'][3]['fcstValue']
                #sky value : 맑음(1), 구름조금(2), 구름많음(3), 흐림(4)
        except TypeError :
            print('날씨 정보가 제공되지 않고 있습니다. ㅠ_ㅠ 잠시 후 다시 시도해주세요')
            exit()
            
        if self.event_type == self.FINE_DUST:
            try:                 
                self.dust_value = self.data["list"][0]['pm10Value']

                #WHO 기준으로 미세먼지 등급 판단
                if 0 <= int(self.dust_value) <= 30:
                    self.dust_grade = 1
                if 31 <= int(self.dust_value) <= 50:
                    self.dust_grade = 2
                if 51 <= int(self.dust_value) <= 100:
                    self.dust_grade = 3
                if 101 <= int(self.dust_value) <= 500:
                    self.dust_grade = 4


                #등급	좋음	보통	나쁨	매우나쁨
                #Grade 값	1	2	3	4

            #미세먼지 데이터가 수집되지 않을 경우 오류처리
            except ValueError:
                pass

           

