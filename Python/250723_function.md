# 함수



## Docstring

- 함수의 body 앞에 선택적으로 작성하는 함수의 사용설명서
- 일반적으로 아래와 같이 여러 줄 주석으로 작성하며, “”” 오른쪽에서 바로 작성 시작

```python
def make_sum(num_1, num_2):
	"""이 함수는 두 수를 받아
	두 수의 합을 반환하는 함수입니다.
	>>> make_sum(1, 2)
	3	
	"""
```



## 출력과 반환의 구분

- 출력은 말 그대로 화면에 값을 출력하기만 하지, 반환과는 관계가 없음

- 대표적으로 print()는 반환값이 없는 함수

- 함수에 return을 작성하지 않으면 자동으로 None을 반환

  ```python
  return_value = print('hello')
  print(return_value) # None
  ```

- Q1. 이 경우 return값을 할당하기만 하면 될 것 같은데, 실제로 함수가 실행돼서 CLI에 ‘hello’가 표시되네? 파이썬이 실행결과 나온 반환값만 사용하지 않고 실제로 실행결과를 적용하는 이유가 뭐지?

  - 모든 함수는 실행해야만 return이 생기고, python은 실행과 결과를 분리하지 않음
  - 함수가 반환값 할당을 위해 실행되면, 실행중 일어나는 모든 연산은 실제로 메모리에 반영됨
  - 대부분의 언어가 이런 식으로 작동함.



## arguments의 자료형을 강제할 수 있는가?

- 원래는 안 됨

- Docstring이나 typehint( `def greet(name: str, age: int)` )를 통해 권장할 수는 있지만 다른 자료형을 넣는다고 해서 바로 오류가 뜨는 건 아님.

- 실행 안정성을 위해서 굳이 하고 싶다면.. 아래처럼 type을 직접 검사하고 분기처리해서 raise error할 수도 있고

- typeguard, pydantic 등 라이브러리를 활용해서 할 수도 있음

- 다른 정적 언어(Java, C++ 등)들은 python과 달리 컴파일 시점부터 type을 검사함

  ```python
  def greet(name: str, age: int) -> str:
      if not isinstance(name, str):
          raise TypeError("name must be a string")
      if not isinstance(age, int):
          raise TypeError("age must be an integer")
      return f"{name} is {age} years old."
  ```



## 재귀함수(recursive function)

- 함수 내부에서 자기 자신을 호출하는 함수
- 언젠가는 끝나야 하니까 앞쪽에 종료조건이 필요하다.
- 1개 이상의 base case(종료조건)을 설정하고, 함수가 반복되면서 거기로 수렴하도록 코드를 짜야 한다.



### 재귀함수의 특징

- 변수의 사용이 줄어들고 코드의 가독성이 높아짐

- 메모리 사용량이 많아 느리고 오버플로우의 가능성이 있음

  

```python
def factorial(n):
	if n == 1:
		return 1
	else:
		return n * factorial(n-1)
```

- Q2-1. 꼭 종료조건으로 수렴해야 하나? 값이 튀다가 종료조건으로 갈 수도 있을 것 같은데..
  - 맞음. 단조수렴(점차 종료조건에 수렴하는 형태)이 가장 일반적이긴 한데, 비단조적으로 설정하는 것도 가능함.
  - 근데 비단조적이더라도 시행횟수가 유한해서 언젠가 종료조건에 도달하는 것이 보장되어야 오버플로우가 안 나겠지.
- Q2-2. 근데뭐 쓰기 나름이니까.. 종료되지 않는 재귀더라도 그냥 flag 걸어서 일정 횟수 후에 종료되도록 할수도 있는 거고(크게 보면 이것도 단조수렴이긴 하겠지만), 아예 끝나지 않더라도 그 과정을 로깅하는게 의미가 있는 작업일 수도 있으니까 무조건 뭐만 맞다고 할 수는 없겠네
  - 그치. 헬스체크나 모니터링 등 의도된 비종료 재귀함수들도 있고, 항상 함수의 return값만 중요한게 아니라 실행되는 과정 자체가 의미가 있는 경우도 있고. 네 말대로 다 쓰기 나름임.



## lambda 표현식

- 한 줄 짜리 간단한 익명함수를 만드는 표현식

  ```python
  def add(x, y):
  	return x + y
  	
  lambda x, y  : x + y
  ```

  ```python
  addition = lambda x, y : x + y
  result = addition(3,4)
  print(result) # 7
  ```

  ```python
  # 이름 길이 기준으로 정렬
  names = ['kim', 'lee', 'park']
  sorted_names = sorted(names, key=lambda x: len(x))
  print(sorted_names)  # ['kim', 'lee', 'park']
  ```

  ```python
  # map함수 응용
  numbers = [1,2,3,4,5]
  
  def square(num):
  	return num ** 2
  	
  squared_1 = list(map(square, numbers))
  print(squared_1)
  
  squared_2 = list(map(lambda num: num ** 2, numbers))
  ```