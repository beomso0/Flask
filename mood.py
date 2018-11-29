#%%
#mood

class Mood(object):

    def __init__(self):
        Mood.self = self

    def decision(self, now, fore, dust):
        temp = now.temp
        humidity = now.humidity

        try : 
            dust = dust.dust_grade
        #값이 없을 경우 오류처리
        except AttributeError : 
            print('미세먼지 정보가 없습니다 ㅠ_ㅠ ')
            exit()

        rain = now.rain
        
        mood_list = []

        #오류 처리를 위해 범위 설정     **기상청 api는 관측 데이터가 없을 경우 '-999', '998' 등 값 반환.
        if -100 < temp <= 5:
            mood_list.append('cold')

        if 28 <= temp < 100:
            mood_list.append('hot')

        try : 
            if dust != None:
                if dust == 3:
                    mood_list.append('bad_d')
                
                if dust == 4:
                    mood_list.append('Vbad_d')
        #오류처리
        except ValueError : 
            print('미세먼지 정보가 없습니다 ㅠ_ㅠ')
            exit()
        
        if 80 <= humidity <= 100:
            mood_list.append('hum')
            
        if 0 <= humidity <= 30:
            mood_list.append('dry')
            
        if rain == 1:
            mood_list.append('rain')
            
        if rain == 3:
            mood_list.append('snow')
            
        self.mood_list = mood_list
        
        return self.mood_list