#%%
# article 생성

import random 
import json 
from retprinter import Retprinter

r = Retprinter()

#날씨 기사 템플릿
w_atc_tmp = {
    'hot' : {
        'full' : ' 기온은 섭씨 {}도로 덥습니다. 온열 질환에 유의의하세요.', 
        'f_half' : ' 기온은 섭씨 {}도로 더우며, ',
         's_half' : '기온은 섭씨 {}도로 덥습니다. 온열 질환에 유의할 필요가 있겠습니다.'
    },
    'cold' : {
        'full' : ' 기온은 섭씨 {}도로 춥습니다. 방한에 유의할 필요가 있겠습니다.', 
        'f_half' : ' 기온은 섭씨 {}도로 추우며, ',
         's_half' : '기온은 섭씨 {}도로 춥습니다. 방한에 유의할 필요가 있겠습니다.'
    },
    'bad_d' : {
        'full':' 미세먼지 농도는 {} 단계입니다. 불필요한 외출을 삼가는 것이 좋겠으며, 부득이한 외출 시에는 마스크 잊지 마세요!', 
        'f_half':' 미세먼지 농도는 {} 단계이며, ',
        's_half':'미세먼지 농도는 {} 단계입니다. 불필요한 외출을 삼가는 것이 좋겠으며, 부득이한 외출 시에는 마스크 잊지 마세요!'
    },
    'Vbad_d' : {
        'full':' 미세먼지 농도는 {} 단계입니다. 불필요한 외출을 삼가는 것이 좋겠으며, 부득이한 외출 시에는 마스크 잊지 마세요!', 
        'f_half':' 미세먼지 농도는 {} 단계이며, ',
        's_half':'미세먼지 농도는 {} 단계입니다. 불필요한 외출을 삼가는 것이 좋겠으며, 부득이한 외출 시에는 마스크 잊지 마세요!'
    },
    'hum' : {
        'full':' 습도는 {}%로 상당히 습합니다.',
        'f_half':' 습도는 {}%로 상당히 습하며, ',
        's_half':'습도는 {}%로 상당히 습합니다.'
    },
    'dry' : {
        'full':' 습도는 {}%로 상당히 건조합니다.',
        'f_half':' 습도는 {}%로 상당히 건조하며, ',
        's_half':'습도는 {}%로 상당히 건조합니다.'
    },
    'rain' : {
        'full':'에는 {} 내리고 있습니다. 우산 잊지 마세요!',
        'f_half':'에는 {} 내리고 있으며, ',
        's_half':'{} 내리고 있습니다. 우산 잊지 마세요!',
    },
    'snow' : {
        'full':'에는 {} 내리고 있습니다. 우산 잊지 마세요!',
        'f_half':'에는 {} 내리고 있으며, ',
        's_half':'{} 내리고 있습니다. 우산 잊지 마세요!',
    },
    'generic':{
        'full':'오늘은 야외활동에 지장이 없는 쾌적한 날씨입니다. 현재 {} 기온은 {}도, 미세먼지 농도는 {}입니다.'
    }
  }

#음식 추천 기사 템플릿
f_atc_tmp = {
    'hot' : ' 오늘같이 더운 날, {} 드시고 힘내세요! 주위에 이런 가게들이 있습니다 :)', 
    'cold' : ' 추운 날에는 역시 {}! 주위에 이런 가게들이 있습니다 :)',
    'Vbad_d' : ' 뿌연 하늘로 지친 마음, {} 드시며 달래보세요! 주위에 이런 가게들이 있습니다 :)',
    'bad_d' : ' 뿌연 하늘로 지친 마음, {} 드시며 달래보세요! 주위에 이런 가게들이 있습니다 :)',
    'hum' : ' 꿉꿉한 오늘 ㅠ_ㅠ 맛있는 {} 드시고 기분전환 해보시는 건 어떨까요? 주위에 이런 가게들이 있습니다 :)',
    'dry' : ' 날씨는 건조하지만 위장은 건조하지 않게! {}은 어떠신가요? 주위에 이런 가게들이 있습니다 :)',
    'rain' : ' 빗소리를 들으면 {} 생각나지 않으시나요? 주위에 이런 가게들이 있습니다 :)',
    'snow' : ' {} 든든히 드시고, 오랜만에 천천히 눈을 맞으며 겨울을 즐겨보세요! 주위에 이런 가게들이 있습니다 :)',
    'generic' : ' 뭘 먹어도 좋을 날씨인 오늘! 오늘 메뉴는 {} 어떠신가요? 주위에 이런 가게들이 있습니다!'
 }

class Article(object):
       
    def __init__(self, mood, locator, n_events,f_events,d_events):
        self.mood_list = mood.mood_list
        self.loca_name = locator.loca_name
        self.now = n_events
        self.fore = f_events
        self.dust = d_events
        self.loca_list = locator.loca_list

    def generate(self):
        
        #weather article 만들기
        
        w_atc_base = '현재 {}'.format(self.loca_name)   
        desc = {
            'cold' : self.now.temp,
            'hot' : self.now.temp,
            'hum' : self.now.humidity,
            'dry' : self.now.humidity,
            'bad_d' : '나쁨',
            'Vbad_d' : '매우나쁨',
            'rain' : '비가',
            'snow' : '눈이'
         } 
        
        if len(self.mood_list) == 0:
            w_article = w_atc_tmp['generic']['full'].format(self.loca_name, self.now.temp,self.dust.dust_value)
        
        # 기온 정보를 모든 기사에 필수적으로 포함하기 위해 if문 추가. 
        if (len(self.mood_list) >= 1) and ('hot' not in self.mood_list) and ('cold' not in self.mood_list):
            if len(self.mood_list) == 1 :
                w_article = (w_atc_base + w_atc_tmp[self.mood_list[0]]['full'].format(desc[self.mood_list[0]]) + 
                           ' 현재 기온은 섭씨 {}도입니다.'.format(self.now.temp))
            
            #mood가 두 개 이상일 경우 랜덤으로 두 개 추출.
            elif len(self.mood_list) >= 2 :
                multi_list = self.mood_list
                random.shuffle(multi_list)
                selec_mood_list = multi_list[0:2]
                w_article = (w_atc_base + w_atc_tmp[self.mood_list[0]]['f_half'].format(desc[self.mood_list[0]]) + 
                           w_atc_tmp[self.mood_list[1]]['s_half'].format(desc[self.mood_list[1]]) + 
                           ' 현재 기온은 섭씨 {}도입니다.'.format(self.now.temp))
            
        else:
            if len(self.mood_list) == 1 :
                w_article = w_atc_base + w_atc_tmp[self.mood_list[0]]['full'].format(desc[self.mood_list[0]])
            
            elif len(self.mood_list) >= 2 :
                multi_list = self.mood_list
                random.shuffle(multi_list)
                selec_mood_list = multi_list[0:2]
                w_article = (w_atc_base + w_atc_tmp[selec_mood_list[0]]['f_half'].format(desc[selec_mood_list[0]]) + 
                           w_atc_tmp[selec_mood_list[1]]['s_half'].format(desc[selec_mood_list[1]]))
        
        #menu_article 만들기

        #미리 만들어둔 {mood : [menus]} 딕셔너리 호출
        json_data = []
        with open("menu_list.json", encoding = 'utf-8') as file:
            data = file.readlines()
            for d in data:
                json_data.append(json.loads(d))
        menu = json_data[0]
        
        if len(self.mood_list) == 0 :
            selec_mood = random.sample(list(menu.keys()),1)
            selec_mood = selec_mood[0]
            selec_menu = random.sample(menu[selec_mood],1)
            selec_menu = selec_menu[0]
            f_article = f_atc_tmp['generic'].format(selec_menu) + '\n\n'

            ret_dict = r.retprint(self.loca_list, selec_menu)
            r_article = ''
            for key, value in ret_dict.items():
                r_article = r_article + key + ' | ' + value + '\n'
            r_article = r_article[:-1]
        
        if len(self.mood_list) == 1 :
            selec_mood = self.mood_list
            selec_mood = selec_mood[0]
            selec_menu = random.sample(menu[selec_mood],1)
            selec_menu = selec_menu[0]
            f_article = f_atc_tmp[selec_mood].format(selec_menu) + '\n\n'

            ret_dict = r.retprint(self.loca_list, selec_menu)
            r_article = ''
            for key, value in ret_dict.items():
                r_article = r_article + key + ' | ' + value + '\n'
            r_article = r_article[:-1]
        
        elif len(self.mood_list) >= 2:

            selec_mood = random.sample(selec_mood_list,1)
            selec_mood = selec_mood[0]
            selec_menu = random.sample(menu[selec_mood],1)
            selec_menu = selec_menu[0]
            f_article = f_atc_tmp[selec_mood].format(selec_menu) + '\n\n'

            ret_dict = r.retprint(self.loca_list, selec_menu)
            r_article = ''
            for key, value in ret_dict.items():
                r_article = r_article + key + ' | ' + value + '\n'
            r_article = r_article[:-1]
        
        return (print(w_article + f_article + r_article))