# 정적 페이지 웹스크래핑 : 요청한 url에서 응답받은 html을 그대로 사용(렌더 : 화면에 보이는 형태로 변환)한 경우
#  - 서버사이드렌더 : 서버에서 html 생성
# requests, beautifulsoup 패키지 이용

# 동적 페이지 웹스크래핑 : 요청한 url에서 응답받은 html 안의 Javascript를 실행해서 html을 새로 만든 경우
#  - 클라이언트사이드렌더 : 클라이언트에서 html 생성

import requests # 파이썬에서 http 요청(웹)을 쉽게 작성
import bs4 # beautifulsoup은 html이나 xml을 parsing해서 데이터를 추출

# 파이썬 할 때는 되도록 버전정보 확인하면서 하는게 좋음. major.minor.patch 넘버인데 major번호가 바뀌면 신경좀 써야됨
print(requests.__version__)
print(bs4.__version__)

def web_request(url):
    url = 'https://naver.com'
    response = requests.get(url)
    # print(response) # <Response [200]> 객체만 전달됨
    # print(response.status_code) # 200 코드만 전달됨
    # print(response.text) # ctrl+U하면 보이는 걔네가 날아온거
    return response.text # 이걸 저장하면 밑에 있는 sample.html같은게 나오는 거겠네

# url = 'https://naver.com'
# html = web_request(url)


from bs4 import BeautifulSoup
with open('../_03_static_webpage/sample.html','r',encoding = 'utf-8') as f:
    html = f.read() # ()안의 인자는 size. 문자나 byte 단위인 듯. default는 전부 다 읽는 거고
bs = BeautifulSoup(html, 'html.parser')
# print(type(bs)) # <class 'bs4.BeautifulSoup'>
# print(bs)

# find / find_all : html 태그 및 속성을 dict로 조회
# select_one / select : css선택자 문법 조회
def test_find():

    tag = bs.find('li')
    print(type(tag)) # <class 'bs4.element.Tag'>
    print(tag)

    tags = bs.find_all('section')
    print(tags)
    print(len(tags))
    tags = bs.find_all('section', 'section1')
    print(tags)

# test_find()

def test_select():
    # css 선택자 : 특정 tag를 찾기 위한 표현식.
    # css에서 공백은 후손 의미, >는 직계자식 의미
    # https://www.w3schools.com/cssref/css_selectors.php
    # 태그만 그대로 사용
    # id #아이디
    # class .클래스
    tag = bs.select_one('section#section2')
    print(type(tag))
    print(tag)

    tags = bs.select('section-content')
    print(tags)

# test_select()

def get_content():
    # section#section2 li
    tags = bs.select('section#section2 li')
    print(tags)

    for tag in tags:
        print(tag.text)

# get_content()

print('-'*30)

# section#section1 하위의 hi태그 내용, p태그내용 출력
def get_content2():
    tags = bs.select('section#section1 h2')
    tags2 = bs.select('section#section1 p')
    for tag in tags:
        print(tag.text)
    for tag2 in tags2:
        print(tag2.text)

# get_content2()

def get_content3():
    h2_tag = bs.select_one
    print('h : ', h2_tag.text)

    p_tags = bs.select('section#section1 p')
    for p_tag in p_tags:
        print('p : ', p_tag.text)

# get_content3()

print('-'*30)

def get_content4():
    # 자식태그 조회
    section1_tag = bs.select_one('section#section1')
    # 특정 태그 하위에서 조회
    h2_tag = section1_tag.select_one('h2')
    print(h2_tag.text)
    p_tags = section1_tag.select('p')
    print([p_tag.text for p_tag in p_tags])

    # 모든 자식 태그 죄회
    children = section1_tag.findChildren()
    print(children)
    for child_tag in children:
        print(child_tag.text)


# get_content4()

