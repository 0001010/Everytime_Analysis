from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time 
from konlpy.tag import Kkma
import openpyxl
import pandas as pd

    
id_pw = pd.read_csv('id_pw.csv',encoding = 'euc-kr')
# 엑셀 작업화
excel_file = openpyxl.Workbook()
excel_sheet = excel_file.active
 
ident = id_pw['id'].to_list()[0]
passw = id_pw['passwa'].to_list()[0]

# selenium으로 자동 로그인
chromedriver ='C:/Users/User/Downloads/chromedriver_win32 (2)/chromedriver'
driver = webdriver.Chrome(chromedriver)
driver.get('https://everytime.kr/login')
driver.find_element_by_name("userid").send_keys(ident)
driver.find_element_by_name("password").send_keys(passw)
driver.find_element_by_xpath('//*[@class="submit"]/input').click()

# 핫게시판 들어가기
time.sleep(2)
driver.find_element_by_xpath('//*[@id="container"]/div[3]/div[2]/div/h3/a').click()
time.sleep(3)
#driver.find_element_by_css_selector('#container > div.wrap.articles > div.pagination > a').click()
 
# 페이지 넘기면서 공감수, 내용, URL, 날짜저장
def next_page():
    time.sleep(0.5)
    
    res = driver.page_source
    soup = BeautifulSoup(res,"html.parser")
    # data_name = soup.select('#container > div.wrap.articles > article > a > h2')
    data_num = soup.select('.vote') # 공감수
    data_text = soup.select('#container > div.wrap.articles > article > a > p') # 게시글의 내용
    data_url = soup.select('#container > div.wrap.articles > article > a') # 게시글의 URL
    data_date = soup.select('time') # 날짜
    for num,text,url,date in zip(data_num,data_text,data_url,data_date):
        excel_sheet.append([int(num.get_text()),text.get_text(),'https://everytime.kr'+url.get('href'), date.get_text()])   
    
    driver.find_element_by_css_selector('#container > div.wrap.articles > div.pagination > a.next').click()
    #num,name,text,url 이라는 폴더에 (공감수, 제목, 내용, url) 각각 넣고 튜플로 저장

# next_page를 30번 반복
for page_roof in range(30):
    if page_roof==0:
        driver.find_element_by_xpath('//*[@id="sheet"]/ul/li[3]/a').click() #뜨는 광고창 끄기
        next_page()
    else:
        next_page()

# everytime crawing 라는 엑셀 파일에 저장
excel_file.save('everytime crawing.xlsx')
excel_file.close()

driver.quit()

