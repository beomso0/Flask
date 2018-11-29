#%%
#Locator

import requests
import json
import math

class Locator():
    
    def __init__(self):
        Locator.self = self
    
    #카카오 로컬 API를 활용해, string 주소명을 경위도로 변환
    def locator(self,loca_name):
        header = {
                'Authorization': 'KakaoAK 40b9edeb2782a7641f9f861453667c8e'
                }
        params = {
            'query' : loca_name,
        }
        url = "https://dapi.kakao.com/v2/local/search/address.json"
        b = requests.get(url, headers=header, params = params)
        bjson = b.json()
        try:
            X = bjson['documents'][0]['x']
            Y = bjson['documents'][0]['y']
        # 주소가 검색되지 않을 경우 오류 처리
        except IndexError :
            print('주소를 다시 확인해주세요 :)')
            exit()
        loca_list = [X,Y]
        self.loca_name = loca_name
        self.loca_list = loca_list     
        return self.loca_list, self.loca_name

    #tm 좌표로 변환
    def to_tm(self):
        loca_list = self.loca_list
        header = {
    'Authorization': 'KakaoAK 40b9edeb2782a7641f9f861453667c8e'
    }
        params = {
            'input_coord' : 'WGS84',
            'output_coord' : 'TM',
            'x' : str(loca_list[0]),
            'y' : str(loca_list[1])

        }
        url = "https://dapi.kakao.com/v2/local/geo/transcoord.json"
        a = requests.get(url, headers=header, params = params)
        ajson = a.json()
        tm_x = ajson['documents'][0]['x']
        tm_y = ajson['documents'][0]['y']
        tm_list = [tm_x,tm_y]
        self.tm_list = tm_list
        return self.tm_list
    
    # 위경도를 기상청 격자 좌표로 변환(v1:위도, v2:경도)
    # 아래의 수식은 기상청 웹페이지에 탑재된 변환기의 javascript 코드를 수정한 것임.
    def to_xy(self):
        
        v1 = self.loca_list[1]
        v2 = self.loca_list[0]   
        
        #LCC DFS 좌표변환을 위한 기초 자료
        RE = 6371.00877  #지구 반경(km)
        GRID = 5.0  #격자 간격(km)
        SLAT1 = 30.0  #투영 위도1(degree)
        SLAT2 = 60.0  #투영 위도2(degree)
        OLON = 126.0  #기준점 경도(degree)
        OLAT = 38.0  #기준점 위도(degree)
        XO = 43   #기준점 X좌표(GRID)
        YO = 136   #기1준점 Y좌표(GRID)
        v1 = float(v1)
        v2= float(v2)
        DEGRAD = math.pi/180
        RADDEG = 180/math.pi
        re = RE / GRID
        slat1 = SLAT1 * DEGRAD
        slat2 = SLAT2 * DEGRAD
        olon = OLON * DEGRAD
        olat = OLAT * DEGRAD
        sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
        sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
        sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
        sf = math.pow(sf, sn) * math.cos(slat1) / sn
        ro = math.tan(math.pi * 0.25 + olat * 0.5)
        ro = re * sf / math.pow(ro, sn)
        rs = {}
        rs['lat'] = v1
        rs['lng'] = v2
        ra = math.tan(math.pi * 0.25 + v1 * DEGRAD * 0.5)
        ra = re * sf / math.pow(ra, sn)
        theta = v2 * DEGRAD - olon
        if theta > math.pi:
            theta -= 2.0 * math.pi
        elif theta < -math.pi:
            theta += 2.0 * math.pi
        theta *= sn
        rs['x'] = math.floor(ra * math.sin(theta) + XO + 0.5)
        rs['y'] = math.floor(ro - ra * math.cos(theta) + YO + 0.5)
        self.xy_dict = rs
        return self.xy_dict