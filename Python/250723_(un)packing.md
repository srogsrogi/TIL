# 패킹 | 언패킹

![image](/image.png)

## 패킹

- 여러 개의 값을 하나의 컬렉션으로 묶는 동작

- 한 변수에 ,로 구분된 값을 넣으면 자동으로 튜플로 처리

  ```python
  packed_values = 1,2,3,4,5
  print(packed_values) # (1,2,3,4,5)
  print(type(packed_values)) # tuple
  ```

### 함수 매개변수 작성시 * 패킹

- `*args`로 임의의 인자를 처리하는 경우 tuple로 묶어서 처리
- `**kwargs`로 임의의 키워드 인자를 처리하는 경우 dict로 묶어서 처리

## 언패킹

- 컬렉션에 담겨 있는 개별 요소를 펼쳐놓는 과정

  ```python
  packed_values = 1,2,3,4,5
  a,b,c,d,e = packed_values # unpack
  print(a,b,c,d,e) # 1 2 3 4 5
  ```

### 함수 인자 전달시 * 언패킹

- 리스트/튜플 앞에 *를 붙여 각 요소를 함수의 개별 위치 인자로 전달

  ```python
  def func(x, y, z):
  	print(x, y, z)
  
  names = ['alice', 'jane', 'peter']
  func(*names) # alice jane peter
  ```

- dict 앞에 **를 붙여 key = value 형태의 키워드 인자로 전달

  ```python
  def func(x, y, z):
  	print(x, y, z)
  	
  my_dict = {'x' : 1, 'y' : 2, 'z' : 3}
  func(**my_dict) # 1 2 3
  ```

- 변수 할당시 언패킹

  - pop()과 유사하게 동작함

  ```python
  my_list = [1, 2, 3, 4, 5]
  a, *b = my_list
  print(a) # 1
  print(b) # [2,3,4,5]
  *a, b = my_list
  print(a) # [1,2,3,4]
  print(b) # 5
  a, *b, c = my_list
  print(a) # 1
  print(b) # [2,3,4]
  print(c) # 5
  ```

## 소감

- python 자체를 처음 배울 땐 그냥 ''저런 것도 있나 보다~' 하고 넘어갔는데..
- 다시 배우니까 좀 보인다. 이번에 연습좀 해두면 계속 잘 쓸 듯