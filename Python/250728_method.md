# 메서드

- 대부분 여러 차례 써본 것들이라 문법 및 특이사항은 노션에 정리함
- https://www.notion.so/SSAFY-bc6a721139f14e0c8de66459a7fd7ddc?p=23e7a051cee680acbf30cfd879d71490&pm=s



## list 메서드 pop() 사용시 주의사항

- 반복문에서 list.pop()을 사용하면, pop할 때마다 인덱스 정보가 바뀌기 때문에 원하는 대로 동작하지 않고 중간중간 요소를 건너뛰게 됨

- 이 문제를 해결하기 위해 쓰는 대표적인 방법은 뒤에 있는 요소부터 pop하는 것

- `for i in range((len(lst)-1), -1, -1):`는 리스트를 거꾸로 순회하고 싶을 때 자주 쓰는 패턴이니 기억해둘 것

  ```python
  def even_elements(lst : list):
      list_result = []
      for i in range((len(lst)-1), -1, -1):
          if lst[i] % 2 == 1:
              lst.pop(i)
          else:
              pass
      list_result.extend(lst)
      return list_result
  ```

  





## 질문/답변

- **Q1. 그럼 파이썬 내장 메서드들도 클래스만 찾아가서 파일을 수정해주면 다 커스터마이징할 수 있겠네?**

  - 이론상 완전 불가능한 건 아니지만 당연히 절대 안 쓰는 방법임

  - python은 내부적으로 C로 구현되어 있고 직접 소스코드를 건드리는 건 허용되지 않음

  - 내장 클래스를 상속받아 자식 클래스를 만든 후 오버라이딩하면 local하게 커스터마이징 가능

- **Q2. 파이썬이 내부적으로 정의한 클래스에서 None을 저렇게 처리한다는 거지? None을 왜 저런 구분자로 사용하지? None의 원래 의미와 좀 괴리가 있는 것 같은데..**
  - 맞고, 좀 특이한 방식이긴 함.
  - 파이썬은 기본값 미지정 flag를 `None`으로 주는 경우가 꽤 있음(sort, sorted의 key 인자 등)
- `'seperator'.join(iterable)`
  - iterable의 문자열을 연결한 문자열을 반환

- **Q3. 하나만 추가하는 append, 여러 개 추가하는 extend가 있는 것처럼, 삽입도 iterable을 순회하면서 삽입하는 메서드는 없나?**

  - 없음. 물론 직접 구현은 가능

    - 슬라이싱

      ```python
      lst = [1, 2, 3]
      lst[1:1] = [9, 9]
      print(lst)  # [1, 9, 9, 2, 3]
      ```

    - 반복문 사용

      - 인덱스는 앞에서부터 세기 때문에 `reverse` 를 통해 요소를 뒤에서부터 추가해야 반복문이 돌 때도 인덱스를 유지함

      - 다른 케이스도 인덱스를 기준으로 하는 함수(`pop` 등)를 쓰는 경우에는 고려해서 사용할 것

        ```python
        lst = [1, 2, 3]
        items = [9, 9]
        for item in reversed(items):
            lst.insert(1, item)
        print(lst)  # [1, 9, 9, 2, 3]
        ```

    - 커스텀 함수 만들기

      ```python
      def insert_many(lst, index, values):
          lst[index:index] = values
      a = [1, 2, 5]
      insert_many(a, 2, [3, 4]) # inplace 연산
      print(a) # [1, 2, 3, 4, 5]
      ```

- **Q4. replace할 때 대소문자 구분 안 하고 다 바꾸고 싶으면 소문자도 replace하고 별개로 uppercase도 replace하는 식으로 반복 호출하는 방법밖에 없나?**
  - 그게 제일 일반적임
  - 정규표현식 re모듈에서 sub함수의 ignorecase인자를 사용하면 동시 처리 가능
    - 다만 입력시 대소문자 구분을 없앨 뿐이고 대문자를 대문자로, 소문자를 소문자로 변환하려면 분기처리 필요
    - re 호출해서 그렇게 구현할 바에는 그냥 replace 분기처리해서 반복호출하는게 나음

- **Q5-1. map이나 zip 이터레이터에 대해 list함수로 변환할 때는 잘 됐는데, reversed 객체를 str함수로 변환하는 건 왜 안 되지?**

  - str로 변환하고 싶을 때는 ‘’.join(iterable)의 형태를 써야 함
  - iterator 안에는 그걸 풀었을 때의 최종 산출물에 대한 직접적인 정보가 들어있지 않으니 직접 문자열로 변환하는 게 불가능함
  - 그래서 join함수를 통해 이터레이터를 소모시켜 전체 문자열을 나타내는 개별 요소를 생성한 뒤에, join함수로 그걸 연결하는 것

  **Q5-2. 그럼 list 변환은 왜 되는 거야?**

  - str()과 list()는 애초에 목적과 내부동작이 다 다름
    - 비유적으로 표현하자면, list()는 객체를 풀어내서 재조합하는 동작이지만 str()는 단순히 객체를 문자열로 표현하는 동작임
    - 따라서 str()는 이터레이터를 소모시키지 않는 함수라서 join()으로 이터레이터를 소모시켜주는 거고, list()는 자체적으로 이터레이터를 소모시켜주는 함수니까 추가 작업을 요구하지 않는 것