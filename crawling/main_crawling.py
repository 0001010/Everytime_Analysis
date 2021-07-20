from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time 
from konlpy.tag import Kkma
import openpyxl
import pandas as pd
import os
from sub_crawling import sub_crawling


id_pw = pd.read_csv('id_pw.csv',encoding = 'euc-kr')
et_cr = pd.read_excel('everytime crawing.xlsx', header = None)
et_cr.rename(columns = {
    0 : 'vote', 1 : 'text', 2 : 'url', 3 : 'date'
},inplace = True)

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

for url_num in range(len(et_cr['url'])):
    time.sleep(0.5)
    
    driver.get(et_cr['url'][url_num])
    time.sleep(2)
    
    res = driver.page_source
    soup = BeautifulSoup(res,"html.parser")
    
    data_num = soup.select('.vote') # 공감수
    data_text = soup.select('#container > div.wrap.articles > article > a > p') # 게시글의 내용
    data_date = soup.select('time') # 날짜
    data_board = soup.select('#container > div.wrap.title > h1 > a') # 게시판 종류
    
    for num,text,date,board in zip(data_num,data_text,data_date,data_board):
        excel_sheet.append([int(num.get_text()),text.get_text(), date.get_text(), board.get_text()])  
    
    if url_num%10==0:
        print(str(url_num)+'/'+str(len(et_cr['url'])))
    else:
        pass
    
excel_file.save('everytime crawing main.xlsx')
excel_file.close()

driver.quit()