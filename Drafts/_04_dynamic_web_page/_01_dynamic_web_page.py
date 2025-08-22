# selenium : 웹 어플리케이션 UI 테스트 도구. python, java, c#, ruby 등 지원
# 특정 웹페이지와 상호작용하며 데이터의 입출력, 브라우저 내 여러 이벤트(클릭, 스크롤...) 지원
# 인증을 요구하는 특정 웹페이지의 데이터 스크랩
# 무한 댓글 스크랩
# 브라우저용 매크로로서 사용 가능
# 크롤링을 불허하는 웹페이지도 있으니 주의

from selenium import webdriver
# 키보드 입력
from selenium.webdriver.common.keys import Keys
# 태그 조회 방식(id, class_name, css_selector, x_path...)
from selenium.webdriver.common.by import By
# 스크롤 처리 등
from selenium.webdriver import ActionChains
# 지연대기
import time

# 1. 크롬 실행
# driver = webdriver.Chrome() # 이것만 써도 가능하도록 업데이트됐는데 지금은 오류 뜨네.
path = 'chromedriver.exe'
service = webdriver.chrome.service.Service(path)
driver = webdriver.Chrome(service=service)
# 2. url 특정 사이트 접속
driver.get('https://naver.com')
time.sleep(1) # 로딩되는 시간은 좀 기다리고 꺼져라. 작업환경이 안 좋으면 시간 좀 늘려야 됨
# 3. 사전 처리 : 검색어 입력 / 버튼 클릭. 여러 개 찾으려면 element -> elements
search_box = driver.find_element(By.ID, 'query')
# print(search_box)
search_box.send_keys('파이썬')
search_box.send_keys(Keys.RETURN)

# 뉴스 버튼 x_path
x_news_btn = '//*[@id="lnb"]/div[1]/div/div[1]/div/div[1]/div[8]/a'
x_next_btn = '//*[@id="lnb"]/div[1]/div/div[1]/div/div[2]/div[2]/a/span'
next_btn = driver.find_element(By.XPATH, x_next_btn)
news_btn = driver.find_element(By.XPATH, x_news_btn)

next_btn.click()
time.sleep(1)
news_btn.click()

# 4. 스크롤 처리 : 화면 스크롤 후 더 많은 데이터 확보
for _ in range(4): # _ 자리에 있는 변수를 다시 안 쓸 거면 _로 써도 됨
    body = driver.find_element(By.TAG_NAME,'body')
    body.send_keys(Keys.END)
    time.sleep(1)

# 5. WebElement 접근 & 데이터 추출
news_contents_elems = driver.find_elements(By.CSS_SELECTOR, '.news_contents')
print(len(news_contents_elems))
time.sleep(1)

for news_contents_elem in news_contents_elems:
    # print(news_contents_elem)
    a_tag = news_contents_elem.find_element(By.CSS_SELECTOR, 'a.news_tit')
    title = a_tag.text
    href = a_tag.get_attribute('href')
    print(title, href)
time.sleep(5)

# pyautogui랑 병용해도 되겠네