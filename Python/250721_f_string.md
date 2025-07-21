# f-string

- python 3.6부터 사용 가능
- f-string의 심화기능을 예제와 함께 자율학습



## 표현식 직접 삽입

- 변수 삽입 뿐 아니라 연산, 함수 호출, 조건식, 포맷팅 등 활용 가능

### 연산

```python
x = 10
y = 5
print(f'{x} + {y} = {x + y}')
```

### 포맷팅

```python
pi = 3.1415926535897932384626433832795028
num = 1234567
print(f'pi = {pi:.2f}') # 3.14
print(f'num = {num:,}') # 1,234,567
```

### 정렬, 너비 지정

- (영)문자 기준으로 정렬하기 때문에 시각적으로는 제대로 정렬이 안 되어 보일 수도 있음
- wcwidth 패키지 사용하면 잘 됨

```python
name = 'Alice'
print(f'[{name:<10}]') # 왼쪽 정렬
print(f'[{name:^20}]') # 가운데 정렬
print(f'[{name:>10}]') # 오른쪽 정렬
```

### 딕셔너리, 리스트 접근

```python
user = {"name": "Alice", "age": 22}
scores = [80, 90, 100]

# dict['key'], list[i]로 요소에 접근
print(f'{user['name']} is {user['age']} years old.')
print(f'Top score: {scores[2]}')
```

### 함수, 메서드 호출

```python
def get_greeting(name):
    return f'Hello, {name}'

print(f'{get_greeting('HG')}, nice to meet you.')
text = 'hello'
print(f'{text.upper()}')
```

### 중괄호 출력

```python
print(f'{{Hello}}') # '{Hello}'
```

### 다중라인 f-string

```python
name = 'HG'
score = 95
print(f'''
학생 정보
--------
이름 : {name}
점수 : {score}
''')
```

### datetime 포맷팅

```python
from datetime import datetime
now = datetime.now()

print(f'{now:%Y-%m-%d %H:%M:%S}')
print(f'{now.strftime('%A, %B %d, %Y')}')
print(f'{now.strftime('%I:%M %p')}')
```

### 조건식

```python
score = 85
print(f'결과 : {'합격' if score >= 70 else '불합격'}')
```

### 정규표현식 조합

```python
import re

text = '이메일 주소 : srsrsr@gmail.com'
match = re.search(r'[\w\.-]+@[\w\.-]+', text)

print(f'추출한 이메일 주소 : {match.group() if match else '없음'}')
```

## 소감

- 몇 개는 이미 알던 거고 새로운 것 중에서도 진짜 괜찮은 것들도 좀 있네..
- 포맷팅이나 함수 호출 같은 건 익숙해지면 잘 써먹을 듯. 정규표현식도 좀 연습해야 되고