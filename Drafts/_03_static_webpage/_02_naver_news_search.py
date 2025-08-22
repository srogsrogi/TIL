# 1. requests로 url 요청 -> html 응답
# 2. BeautifulSoup객체 생성
# 3. li.bx 태그(제일 큰 묶음)를 조회(n개)
# 4. li. > .newscontent > 두 번째 a태그
# 5. text 뉴스제목, href속성값(링크)

import requests
from bs4 import BeautifulSoup
#
# # 검색 url 생성
# # query = input('뉴스 검색 키워드를 입력하세요 : ')
# query = '파이썬'
# url = f'https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query={query}'
#
# # 뉴스검색 요청
# response = requests.get(url)
# html = response.text
# # print(html)
#
# # BeautifulSoup으로 html parsing
# bs = BeautifulSoup(html, 'html.parser')
#
# # 뉴스 블럭 접근
# a_tags = bs.select('a.news_tit')
# print(a_tags)
#
# for a_tag in a_tags:
#     title = a_tag.text
#     href = a_tag['href']
#     print(title)
#     print(href)
#
# # 뉴스 썸네일 이미지 가져오기. 이미지 url 찾아서 download
# # img.thumb 태그를 찾아서 src속성 가져오기
#
# img_tags = bs.select('.news_contents img.thumb')
# img_lazysrc = []
# for img_tag in img_tags:
#     print(img_tag['src'])
# # 빠르게 이미지를 사용자에게 제공하기 위해 이미지 비동기 처리. 소스속성에 실제 image url은 없고 임시이미지가 들어있음
#     img_lazysrc.append(img_tag['data-lazysrc'])
#
# print(img_lazysrc)
#
# # 이미지 다운로드
# img_dir = './images'
# from urllib.request import urlretrieve
# from datetime import datetime
# today = datetime.today().strftime('%y%m%d')
# for i, src in enumerate(img_lazysrc):
#     if src.startswith('http'):
#         urlretrieve(src, f'{img_dir}/{today}_{i}.jpg')
#
# def img_download(src, i):
#     # 이미지 다운로드
#     img_dir = "./images"
#     today = datetime.now().strftime('%y%m%d')
#     filename = f'{img_dir}/{today}{i}.jpg'
#     urlretrieve(src, filename) # 이미지 다운로드
#     return filename
#
#
# 뉴스블럭 가져오기(title, href, img.thumb)
news_contents = bs.select('div.news_contents')
print(len(news_contents)) # 10
for i, news_content_tag in enumerate(news_contents): # 제목, 뉴스링크 함께 가져오기
    a_tag = news_content_tag.select_one('a.news_tit')
    title = a_tag.text
    href = a_tag['href']
# 이미지 가져오기
    img_tag = news_content_tag.select_one('img.thumb')
    img = None
    if img_tag:
        img_lazysrc = img_tag[('data-lazysrc')]
        if img_lazysrc.startswith('http'):
            img = img_download(img_lazysrc, i) # 이미지 다운로드 처리

#    print(title, href, img)


class NewsEntry:
    def __init__(self, title, href, img_path):
        self.title = title
        self.href = href
        self.img_path = img_path

    def __repr__(self):
        return f'NewsEntry(title = {self.title}, href = {self.href}, img_path = {self.img_path}) '

news_entries = []
news_entry = NewsEntry(title, href, img_path)
news_entries.append(news_entry)


for news_entry in news_entries:
    print(news_entry)


# 1. requests url 요청
# 2. html 응답
# 3. BeautifulSoup 객체 생성
# 4. li.bx 태그를 조회 (n개)
# 5. 반복순회 li.bx > .newscontent > 두번째 a태그
# 6. text 뉴스제목, href속성 링크
import requests
from bs4 import BeautifulSoup

# 검색 url 생성
query = "파이썬"
# query = input("뉴스 검색 키워드를 입력하세요 : ")
url = f'https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&sort=1&query={query}'

# 뉴스검색 요청
response = requests.get(url)
html = response.text
# print(html)

# html parsing
bs = BeautifulSoup(html, 'html.parser')

# 뉴스블럭 가져오기 (title, href, img.thumb)
news_contents = bs.select("div.news_contents")
print(len(news_contents))  # 10

from urllib.request import urlretrieve
from datetime import datetime


# 스크랩한 뉴스 정보를 담을 NewsEntry 클래스
class NewsEntry:
    def __init__(self, title, href, img_path):
        self.title = title
        self.href = href
        self.img_path = img_path

    def __repr__(self):
        return f'NewsEntry(title={self.title}, href={self.href}, img_path={self.img_path})'


news_entries = []


def img_download(src, i):
    # 이미지 다운로드
    img_dir = "./images"
    today = datetime.now().strftime('%y%m%d')
    filename = f'{img_dir}/{today}_{i}.jpg'
    urlretrieve(src, filename)  # 이미지 다운로드
    return filename


for i, news_content_tag in enumerate(news_contents):
    # 제목, 뉴스링크 가져오기
    a_tag = news_content_tag.select_one("a.news_tit")
    title = a_tag.text
    href = a_tag['href']

    # 이미지 가져오기
    img_tag = news_content_tag.select_one("img.thumb")
    img = None  # img 초기화
    if img_tag:
        img_lazysrc = img_tag['data-lazysrc']
        if img_lazysrc.startswith('http'):
            img = img_download(img_lazysrc, i)  # 이미지 다운로드 처리

    # print(title, href, img)
    news_entry = NewsEntry(title, href, img)
    news_entries.append(news_entry)

# 결과 출력
for news_entry in news_entries:
    print(news_entry)

"""
# 뉴스블럭 접근
a_tags = bs.select('a.news_tit')
print(len(a_tags))

for a_tag in a_tags:
    title = a_tag.text
    href = a_tag['href']
    print(title, href)

# 뉴스 썸네일 이미지 가져오기
# - 이미지 url 가져와서, 다운로드
# - img.thumb태그를 찾아서 src속성 가져오기
img_tags = bs.select('.news_contents img.thumb')
img_lazysrc = []
for img_tag in img_tags:
    # print(img_tag['src'])
    # 좀더 빠르게 이미지를 사용자에게 제공하기 위해 이미지 비동기처리를 사용하고 있다.
    # src속성에는 실제 이미지 url이 없다.
    # print(img_tag['data-lazysrc'])
    img_lazysrc.append(img_tag['data-lazysrc'])

print(img_lazysrc)

# 이미지 다운로드
img_dir = "./images"

from urllib.request import urlretrieve
from datetime import datetime

today = datetime.now().strftime('%y%m%d')
print(len(img_lazysrc))
for i, src in enumerate(img_lazysrc):
    if src.startswith('http'):
        urlretrieve(src, f'{img_dir}/{today}_{i}.jpg')
"""