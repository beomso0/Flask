#%%
#menu_listjson 만들기 

import pandas as pd
import numpy as np
import json

#메뉴마다 mood를 부여해 놓은 csv파일 호출
data = pd.read_csv('menu_list.csv', encoding='euckr')
data.index = data.menu
data = data.drop(["menu"], axis=1)
data.columns = ['cond1','cond2','cond3','cond4','cond5','cond6','cond7']
data = data.fillna("")

#'mood' : [menu list] 형식의 딕셔너리로 변환
conds = ['cold','hot','high_d','hum','dry','rain','snow']
menu = {}
for cond in conds:
    menus = []
    for idx, row in data.iterrows():
        #idx와 row는 각각 index와 row(각 index의 전체 데이터)  
        if cond in list(row):         
            menus.append(idx)
        if (cond == 'high_d'):
            menu['bad_d'] = menus
            menu['Vbad_d'] = menus
        else:
            menu[cond] = menus

#json 파일로 작성
with open('menu_list.json', 'w', encoding="utf-8") as make_file:
   json.dump(menu, make_file, ensure_ascii=False)