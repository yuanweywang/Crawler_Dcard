from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
import requests

s= Service('./chromedriver')
options = Options()
options.add_argument("--disable-notifications")
chrome = webdriver.Chrome(service=s, options=options)
chrome.get("https://www.dcard.tw/f/relationship")
time.sleep(2)

#搜尋「寂寞」
browser = chrome.find_element(by=By.XPATH, value="//input[@value='']")
browser.send_keys('寂寞')
browser.submit()
time.sleep(2)

#參數初始化
numbers=[]
titles=[]
times=[]
contents=[]
num=238498278

#設定滾動、爬蟲
while num > 232407029 :
    article=chrome.find_elements(by=By.XPATH, value='//h2[@class="sc-dc8defdb-2 exgxvu"]')     
    time.sleep(1)
    for art in article: 
        element= art.find_element(by=By.CSS_SELECTOR, value='a')   
        num = int((element.get_attribute('href'))[-9:])   
        if (num not in numbers )and (232800643<=num<=238498278) :
            numbers.append(num) 

            url='https://www.dcard.tw/f/mood'+'/p/'+str(num)
            web=requests.get(url)
            time.sleep(1)
            soup = BeautifulSoup(web.text, "html.parser") 
            
            time.sleep(1)
                      
            titles.append(soup.find("h1", class_="sc-ae7e8d73-0 wYxxj").get_text()) 
            times.append(soup.find("div", class_="sc-c211271f-4 jBSeNh").next_sibling.get_text())
            contents.append(soup.find("div", class_="sc-ebb1bedf-0 aiaXw").get_text())   

    chrome.execute_script("window.scrollBy(0,450)")
    time.sleep(2)

#製作成datafram
dic={'Number':numbers, 'Title':titles, 'Date':times, 'Content':contents}
df=pd.DataFrame(dic)
print(len(numbers))
#存檔
df.to_csv('Dcard文章資料心情版.csv', encoding ='utf-8-sig', index=False)   
