# List Comprehension

- 기존 iterable을 바탕으로 새로운 리스트를 만드는 간단한 문법
- for문을 한 줄로 줄여줌
- 비슷한 구조로 dict comprehension이나 set comprehension도 있음



## 기본 구조

- `[표현식 for 변수 in 이터러블]`

```python
# ex)
characters = [char for char in 'hello'] # ['h', 'e', 'l', 'l', 'o']
```



## 핵심 패턴



### 1. 조건 filtering

#### 1-1. if

- `[표현식 for 변수 in 이터러블 if 조건식]`

```python
not_odd = [num for num in range(10) if num % 2 == 0] # [0,2,4,6,8]
```

#### 1-2. if - else

- [표현식 if 조건식 else 표현식 for 변수 in 이터러블]

```python
odd_or_even = ['짝수' if num % 2 == 0 else '홀수' for num in range(10)]
```



### 2. nested for문

- [표현식 for 바깥변수 in 바깥이터러블 for 안변수 in 안이터러블]
- 3중 중첩문도 구현은 가능한데 가독성이 너무 떨어져서 안 쓰고 일반 for문으로 씀

#### 2-1. 기본 구조

```python
[(i,j) for i in [1,2] for j in ['a','b']]
# [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
```

#### 2-2. nested for문 + if

```python
# 2중첩리스트의 모든 요소를 순회하며 특정 키워드가 있는지 찾는 함수를 만들어보자

def find_key(nested_list : list):
    [print('key를 찾았습니다.') for outer in nested_list for inner in outer if inner == 'key']
    
words = [['a','b','c'],['d','e','f'],['g','h','i'],['key']]
find_key(words) # key를 찾았습니다.
```

#### 2-3. nested for문 + if-else

- 실제론 복잡한 구조는 comprehension 안 쓰지만 연습용

- break나 flag같은 걸 못 쓰니까 아래 예제처럼 한 줄에 다 구현하기는 쉽지 않음

  ```python
  # 위 예제에 if-else 추가
  def find_key(nested_list : list):
      [print('key를 찾았습니다.') if inner == 'key' else print('key가 아닙니다.') for outer in nested_list for inner in outer]
      
  words = [['a','b'],['key']]
  find_key(words) # key가 아닙니다. key가 아닙니다. key를 찾았습니다.
  ```



### 3. 함수 적용

#### 3-1. 일반 함수 및 메서드 적용

- `[함수(변수) for 변수 in 이터러블]`

```python
def square(number):
    return number ** 2

numbers = [1,2,3,4,5]

squared_numbers = [square(number) for number in numbers]
squared_numbers
```

- `[변수.메서드 for 변수 in 이터러블]`

```python
characters = ['a', 'b', 'c', 'd', 'e']

upper_characters = [char.upper() for char in characters]
upper_characters
```



#### 3-2. lambda 함수 적용

- `[lambda x : 표현식(x) for x in 이터러블]`

```python
list(map(lambda x: x * x, [1,2,3])) # [1,4,9]
```



### 4. 2차원 리스트(행렬) 평탄화

- [변수 for row in 행렬 for 변수 in row]

```python
matrix = [[1,2],[3,4]]
flattened = [x for row in matrix for x in row]
print(flattened) # [1,2,3,4]
```



## 질문/답변

- **Q1. 람다 표현식에서, (lambda x : x * x)(x) 이런 식으로 (x)를 써줘야 하는 이유가 뭐지?** 
  - 앞쪽은 함수 선언부고, (x)를 통해서 같은 행에서 호출을 해주는 거.
  - 이전에 안 썼던 것처럼 느낀 건 map함수랑 같이 썼으니까..
    - map(function, iterable)은 그 자체가 함수를 호출해주니까 그 때는 호출부가 필요없었지
- **Q2. 그럼 선언부에 있는건 인자고 호출부에 있는건 변수란 소리잖아. 서로 다른 이름을 써도 되는 거 아냐? 왜 헷갈리게 같은 이름을 쓰지?**
  - 다른 이름을 써도 물론 잘 작동하지. 그렇게 해도 됨.
  - 나는 아직 구조나 문법이 익숙하지 않으니까 헷갈리는 거고, 같은 이름으로 쭉 써놓으면 가독성이 좋아서 관례적으로 그렇게 씀.
  - 이해한대로, 선언부에서 사용되는 왼쪽 x는 람다 함수 내부의 지역변수고, 호출부에서 사용되는 오른쪽의 (x)는 상위 스코프(보통 전역)에 있는 변수라는 감각을 가지길 바람.