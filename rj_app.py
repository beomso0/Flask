#%%
#기사 생성 어플리케이션

from crawler import Crawler
from locator import Locator
from events import Events
from mood import Mood
from retprinter import Retprinter
from article import Article

# class instance 생성
locator = Locator()
crawler = Crawler()
retprinter = Retprinter()
mood = Mood()

# 지역명 입력 및 좌표 변환
local_name = input('현재 계신 곳의 지역명을 입력해주세요  EX)관악구 봉천동, 서귀포시     ')
locator.locator(local_name)
locator.to_xy()
locator.to_tm()

# 데이터 수집
now_fetch = crawler.now_weather_fetch(locator.xy_dict)
fore_fetch = crawler.fore_weather_fetch(locator.xy_dict)
dust_fetch = crawler.fine_dust_fetch(locator.tm_list)

# 이벤트 처리
now_data = Events(now_fetch,1)
fore_data = Events(fore_fetch,2)
dust_data = Events(dust_fetch,3)
now_data.process_events()
fore_data.process_events()
dust_data.process_events()

#mood decision
mood.decision(now_data,fore_data,dust_data)

#기사 생성
article = Article(mood,locator,now_data,fore_data,dust_data)
try:
    print(article.generate())
except TypeError :
    print('데이터가 제공되지 않고 있습니다 ㅠ_ㅠ')