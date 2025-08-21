# 네이버 검색 API 예제 - 블로그 검색
# https://developers.naver.com/docs/serviceapi/search/blog/blog.md#python
import os
import sys
import urllib.request

# Web Res API 방식 호출. 발급받은 id와 secret 입력
client_id = "qhhduCiB0uKs0OOlUZS9"
client_secret = "orqb3Bnnu8"

#검색어
encText = urllib.parse.quote("김")
display = 100 # 한 번에 몇 개 출력할까? 따로 지정 안 하면 10 되더라
# url에 display를 파라미터로 추가해준 코드로 바꿔야 작동함. 지금은 json만 바뀌어 있음.# 대부분의 api는 50~100개가 최대임
url = f"https://openapi.naver.com/v1/search/news?query={encText}&display={display}" # JSON 결과. 딕셔너리랑 비슷한 형식으로 나옴
# url = "https://openapi.naver.com/v1/search/news.xml?query=" + encText # XML 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
# 실제 요청 후 응답을 받아내는 코드. 최신순으로 가져오넹
response = urllib.request.urlopen(request)
# 응답코드. 200이면 성공, 4xx나 5xx는 실패
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)