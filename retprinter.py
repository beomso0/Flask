#%%
#Retprinter
#카카오 로컬 api를 활용하여, article에서 선정한 메뉴를 판매하는 주변 식당을 검색함. 사용자가 입력한 지역 반영, 정렬은 카카오맵의 '정확도순'.

import json
import requests

class Retprinter(object):
    
    def __init__(self):
        Retprinter.self = self
           
    def retprint(self,loca, menu):
        header = {
    'Authorization': 'KakaoAK 40b9edeb2782a7641f9f861453667c8e'
    }
        params = {
            'query' : menu,
            'category_group' : 'FD6',
            'sort' : 'accuracy',
            'size' : '5',
            'x' : str(loca[0]),
            'y' : str(loca[1])
        }
        
        url = "https://dapi.kakao.com/v2/local/search/keyword.json"
        a = requests.get(url, headers=header, params = params)
        ajson = a.json()
        rlist = {}
        for r in ajson['documents']:
            rlist[r['place_name']] = r['address_name']
        return rlist