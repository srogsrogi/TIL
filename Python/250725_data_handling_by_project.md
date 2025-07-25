# 관통 PJT

- SSAFY 매주 금요일,  2인 1조 5~6시간짜리 미니 프로젝트 진행



## 프로젝트 목표

- AI 기반 도서 분석과 창작 지원 통합 솔루션 서비스를 구축하기 위한 **5개 기능 구현**
  - F06 : 어린이 도서가 아닌 책 찾기
  - F07 : 출판사별 도서 수 집계
  - F08 : 카테고리별 도서 수, 평균 가격 계산
  - F09 : 출판일 기준 최신 도서 10개 목력 리스트로 정리
  - F10 : 할인율이 가장 큰 도서 5개 조회



## 프로젝트 산출물

### 1. F06 : 도서 필터링

- `pathlib`을 활용한 파일 경로 탐색
- JSON 데이터 로드(`with open ...`)
- for문을 활용한 키워드 필터링

#### **주요 코드**

```python
non_children_books = []  # 어린이 도서가 아닌 책을 저장할 리스트
# '어린이' 카테고리가 포함되지 않은 책을 필터링하는 코드
for book in books:
	if '어린이' not in book['categoryName']:
		non_children_books.append(book)
```

### 2. F07 : JSON 데이터 조작 및 연산

- list indexing, dict key를 통해 원하는 값에 접근
- .items(), .keys(), .values() 메소드 활용
- 반복문 + 조건식과 count변수를 활용한 개수 세기
- f-string을 활용하여 출력형식 지정

#### 주요 코드

```python
# 3. 출판사별 도서 수 집계
publisher_counts = {}  # 출판사별 도서 수를 저장할 딕셔너리
for book in books:
    # dict에 해당 출판사명이 key 값으로 존재하면 value를 +1
    if book['publisher'] in publisher_counts:
        publisher_counts[book['publisher']] += 1
    # dict에 해당 출판사명이 아직 없으면 value = 1로 key-value 쌍 생성
    else:
        publisher_counts[book['publisher']] = 1
```

### 3. F08 : JSON 데이터 조작 및 연산(응용)

- F07과 유사한 알고리즘 사용
- 1차원 더 깊은 데이터 형식을 요구

#### 주요 코드(내가 푼 방식)

```python
category_stats = {}  # 카테고리별 통계를 저장할 딕셔너리
    
for book in books:        
    # key를 count_<카테고리명>, price_<카테고리명>으로 하는 key-value 쌍 생성
    key_book_count = f'count_{book["categoryName"]}'
    key_price = f'price_{book["categoryName"]}'

    # 이미 있는 key면 더해주고, 없는 key면 새로 생성
    if key_book_count in category_stats:
        category_stats[key_book_count] += 1
        category_stats[key_price] += book['priceSales']
    else:
        category_stats[key_book_count] = 1
        category_stats[key_price] = book['priceSales']
```

- 접두사를 활용하여 key-value쌍을 book*2개만큼 생성한 후 연산
- `flat dict`라고 불리는 방식
- 구조가 단순하지만 데이터가 논리적으로 묶이지 않아서 이후에 데이터를 조작하거나 추가하기 더 어려움



#### 주요 코드(GPT가 푼 방식)

```python
category_stats = {}  # 카테고리별 통계를 저장할 딕셔너리
for book in books:
    # 'categoryName'과 'priceSales' 키가 있는지 확인
    if 'categoryName' in book and 'priceSales' in book:
            
        category_name = book['categoryName']
            
        # 'categoryName'이 유효한 문자열인지 확인 (비어있지 않은 경우)
        if category_name:
            # 해당 카테고리가 통계 딕셔너리에 없으면 새로 추가
            if category_name not in category_stats:
            	category_stats[category_name] = {'count': 0, 'total_price': 0}
                
            # 도서 수와 가격을 집계
            category_stats[category_name]['count'] += 1
            category_stats[category_name]['total_price'] += book['priceSales']
```

- dict 안에 dict를 생성하여 그 안에서 key-value 쌍을 저장
- `중첩 dict`방식
- 한 차원 깊은 데이터 구조를 가짐
- 카테고리를 기준으로 명확하게 그룹화되어 이후에 데이터를 다루기 쉬움

#### 배운 점

- 코드가 작동하는 것 자체도 중요하지만, 상황과 목적에 맞는 코드를 짜는 것이 좋다.
- 구조를 먼저 생각하지 않고 일단 작동만 하게 짠 코드는 언젠가 재사용할 때 문제를 일으킨다.



### 4. F09 : 날짜 기준 정렬

- sorted 함수 활용
- datetime 모듈 활용

#### 주요 코드

```python
# pubDate의 자료형이 문자열이기 때문에 비교연산을 위해 datetime객체로 변경
for book in books:
    book['pubDate'] = datetime.strptime(book['pubDate'], "%Y-%m-%d")
    
# 내림차순정렬 후 앞 10개만 슬라이싱하여 새 변수에 할당
latest_books = sorted(books, key = lambda x: x['pubDate'], reverse = True)[:10] 
# 4. 결과 출력
print("최신 도서 10개:")
# latest_books의 요소들을 통해 book 조회
for book in latest_books:  # 선택된 도서를 순회하며 출력
    # 도서 제목과 출판일을 출력하는 코드
    # 날짜 출력형식에서 00:00:00을 제거하기 위해 datetime객체를 str로 변경한 후 슬라이싱
    print(f'{book["title"]} - {str(book["pubDate"])[:11]}')

```

#### 배운 점

- sorted함수에 lambda 표현식을 넣어서 새로운 리스트 만들기
- datetime 모듈 사용법
  - datetime객체는 indexing/slicing이 불가능해서 출력형식을 직접 바꾸기 위해 str() 사용
  - 사실 `yyyy-mm-dd` format의 날짜는 str이든 int든 숫자의 특성 때문에 변환 없이 sort해도 됨



### 5. F10 : 커스텀 함수 활용

- 할인율 계산 함수 정의
- 정의한 함수를 반복문에서 호출하여 원하는 값 반환

#### 주요 코드

```python
def calculate_discount_rate(book : dict):
    """도서정보에서 제공하는 정가와 할인가를 통해 할인율을 계산하는 함수입니다.
    (정가 - 원가) / 정가 를 계산합니다."""    
    return (book['priceStandard'] - book['priceSales']) / book['priceStandard'] 

# 도서별 할인율 계산 후 key를 discountRate로 하여 원본 딕셔너리에 할당
for book in books:
    book['discountRate'] = calculate_discount_rate(book)

# 5. 할인율 기준 정렬 및 상위 5개 도서 선택
discounted_books = sorted(books, key = lambda x : x['discountRate'], reverse = True)[:5]

# 6. 결과 출력
print("할인율 상위 5개 도서:")
for book in discounted_books:
    print(f"{book['title']} - 할인율: {book['discountRate']:.2f}%")
```

#### 배운 점

- 커스텀 함수 type hint 및 docstring 작성 연습
- f-string formatting



## 감상

- 프로그래밍 처음 배울 때는 객체지향, 모듈화같은 개념들이 너무 힘들었는데 이번 프로젝트에서 똑같은 코드 몇 번씩 복-붙해보니 왜 배워야하는지 와닿는다.
- AI의 도움을 많이 받지 않고 스스로 고민하면서 성장했다.
  - 문제가 생겼을 때 단계별로 출력해보며 디버깅하는 연습이 잘 이루어졌다.
  - 그간 구조를 이해하지 않고 필요한 데이터만 꺼내서 사용했던 API들을 더 잘 활용할 수 있을 것 같다.
- 팀원과 대화하면서 하니까 혼자 하는 것에 비해 생각이 구조적으로 잘 정리되는 것 같다.

