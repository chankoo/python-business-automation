import requests
from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

# from collections import OrderedDict

if __name__=='__main__':

    daegu = pd.read_csv(input("'shop_no'가 있는 업소리스트 csv파일이름입력하세요:")) # 업소리스트 받아온다
    daegu_shop_no = list(daegu.shop_no) # 업소번호를 리스트로 저장

    driver_path = 'chromedriver.exe' # 크롬드라이버 이용
    driver = webdriver.Chrome(driver_path) # 드라이버 객체생성
    
    gu_to_on ={} # key: 지역구 이름, value: 모두선택 flag
    for _ in range(int(input("추가할 지역구의 개수 입력하세요:"))):
        gu_to_on[input('추가할 지역구를 하나씩 입력후 엔터:')] = False
    
    ##############################################################################
    # 기존 설정된 지역분류 
    # 초기화위해 추가적인 코딩필요
    ##############################################################################
    
    for shop_no in daegu_shop_no:
        # 해당업소 배달권역 설정 페이지로 이동
        driver.get('https://super.smartbaedal.com/admin/shop/shopgeofence.asp?shop={}&so=https%3A%2F%2Fsuper%2Esmartbaedal%2Ecom%2Fadmin%2Fshop%2Fshop%2Easp'.format(shop_no))
        
        #지역구 정보담은 area_tr_4 리스트
        tr4_lst = driver.find_elements_by_css_selector("#area_tr_4")
        
        for tr4 in tr4_lst: # area_tr_4에 대해
            td_lst = tr4.find_elements_by_css_selector('td') # 지역중분류/행정동선택/삭제의 세가지 탭의 리스트를 찾고
            for i,td in enumerate(td_lst): # 세가지 탭에대해
                if i%3==0 and td.text.split()[2] in gu_to_on.keys():  # 첫번째탭(i%3==0)의 지역구가 켜야할 구(gu_to_on)에 있으면
                    td_lst[i+1].find_element_by_class_name('input_check').click() # 모두선택을 클릭해 켜준다
                    for k in gu_to_on.keys():
                        if k == td.text.split()[2]:
                            gu_to_on[k] = True # 플래그를 True로 설정해준다
        
        ##########################
        if all(gu_to_on.values()) == False: # gu_to_on_flag 중 false가 있는 경우 직접 추가해줘야한다
            gu_to_on_false = []
            for k in gu_to_on.keys():
                if gu_to_on[k] ==False:
                    gu_to_on_false.append(k)

            for _ in range(len(gu_to_on_false)):
                driver.find_element_by_css_selector('#area_th > span > input[type="button"]').click() # false인 flag만큼 행정동 추가버튼 클릭
            
            
            # 지역대분류, 소분류 드롭다운 버튼이 false인 flag 수만큼 각각 생성되어 'select' 라는 name을 가짐
            select_lst = driver.find_elements_by_tag_name('select')[:-1] # select el의 리스트 (배달반경 선택 element 제외)

            tmp_lst = [] # select_lst와 쌍맞춰주려 임시 리스트생성
            for el in gu_to_on_true:
                tmp_lst.extend([el,el])
                
            for i,select_el in enumerate(zip(select_lst, tmp_lst)):
                if i%2 == 0: # 지역대분류코드가 들어갈 자리
                    select_rgn1 = Select(select_el[0])  
                    select_rgn1.select_by_value('27') # 27 == 대구광역시
                
                time.sleep(0.3)
                
                else: # 지역중분류코드 자리
                    select_rgn2 = Select(select_el[0]) 
# 여기부터 수도코드
#                     select_rgn2.select_by_visible_text(select_el[1]) # '중구','남구'등 지역구명으로 select
#                     time.sleep(0.3)
                    
#                     # 생성된 동면읍 단위 모두선택
#                     td_lst = select_rgn2.parent.find_elements_by_tag_name('td') # 해당 select element의 parent에 가서 td 리스트 다시찾는다
#                     td_lst[1].find_element_by_class_name('input_check').click() # 모두선택을 클릭해 켜준다
#                     for k in gu_to_on.keys():
#                         if k == td.text.split()[2]:
#                             gu_to_on[k] = True # 플래그를 True로 설정해준다
                    
                    
                    if all(gu_to_on.values()) == True:
                        driver.find_element_by_id('bt_update').click()
                        # 엔터도 쳐줘야함
                    else:
                        print("someting went wrong!!")
                    

