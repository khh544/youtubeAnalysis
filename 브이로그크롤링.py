from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip
import pyautogui
import time
import pandas as pd
# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 메시지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# deprecationwarning 방지
service = Service(executable_path=ChromeDriverManager().install())

#driver_path = ChromeDriverManager().install()
#driver = webdriver.Chrome(driver_path, options=chrome_options)
driver = webdriver.Chrome(service=service, options=chrome_options)
actions = ActionChains(driver)
driver.get("https://www.youtube.com/results?search_query=%EB%B8%8C%EC%9D%B4%EB%A1%9C%EA%B7%B8+after%3A2021-8-22+before%3A2021-10-21")


# infos = driver.find_elements(By.CSS_SELECTOR, '.style-scope.ytd-item-section-renderer>div#dismissible')
# before_infos = len(infos)

# while True:
#     # 맨 아래로 스크롤을 내려준다.
#     driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)

#     # 스크롤 사이 페이지 로딩 시간
#     time.sleep(2)

#     # 스크롤 후 상품 개수
#     infos = driver.find_elements(By.CSS_SELECTOR, ".style-scope.ytd-item-section-renderer>div#dismissible")
#     after_infos = len(infos)

#     if before_infos == infos:
#         break

#     # 스크롤 전 상품 개수 업데이트
#     before_infos = after_infos
last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(3)
    new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    if new_page_height == last_page_height:
        break
    last_page_height = new_page_height


infos = driver.find_elements(By.CSS_SELECTOR, '.style-scope.ytd-item-section-renderer>div#dismissible')
lili=[]
for info in infos:    
    actions.move_to_element(info).perform()
# 제목
    anchor = info.find_element(By.CSS_SELECTOR, 'a#video-title')
    title = anchor.text.strip()
    link = anchor.get_attribute("href")
    
    # 조회수
    views = info.find_element(By.CSS_SELECTOR, 'div#metadata-line>span.style-scope:nth-child(1)').text.strip()
    # 시간
    date = info.find_element(By.CSS_SELECTOR, '.style-scope.ytd-thumbnail-overlay-time-status-renderer#text').text.strip()
    #print(title, sep='\n')
    lili.append([title,link, views,date])

df = pd.DataFrame(data=lili,columns=['제목','링크','조회수','영상길이'])
df.to_excel('vlog.xlsx')
