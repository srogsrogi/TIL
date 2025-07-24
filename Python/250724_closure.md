# Closure

- 원래 CS쪽에서 공부할 법한 개념인데.. GPT한테 lambda함수에 대해 물어보다가 멀리 왔다..

- 스토리텔링을 중심으로 정리



## LEGB 룰에 따르면..

- 안쪽 scope에서 바깥쪽 변수를 수정할 수는 없다.
  - `nonlocal`이나 `global` 키워드를 사용하면 가능
- 그러나 바깥쪽 변수를 조회하는 것은 가능하다.

```python
msg_global = 'global variable'
def outer():
    msg_outer = 'enclosing variable'
    print(msg_global, msg_outer) # global variable enclosing variable

    def inner():
        print(msg_outer) # enclosing variable
        print(msg_global) # global variable

    inner()

outer()
```

## Local 영역에서 어떻게 외부 변수를 참조하는가?

### 1. Enclosing scope

- Local 영역이 생성될 때, closure 속성을 만들고 그 안에 enclosing 영역에서 정의된 변수들을 저장한다. 
  - 각 변수들은 cell object라는 객체(변수가 참조하는 id)로서 속성 내에 저장된다.
  - Local에서 그 변수를 호출하면 closure에 저장된 객체를 참조한다.



### 2. Global / Built-in scope

- Global과 Built-in scope에 있는 변수들에 대해서는 closure 속성을 만들지 않는다.
  - 인터프리터 입장에서 봤을 때, 해당 모듈 내에서 Global과 Built-in 내의 변수들은 이름만 가지고 있으면 언제 어디서든 호출 가능한 변수이기 때문에 특정 Local 안에만 별도로 저장할 필요가 없다.



## 다중 중첩 함수에서 Enclosing scope가 여러 층인 경우는?

- closure는 재귀적이고 누적적으로 확장된다. 무슨말이냐면..

```python
def f1():                 # 함수 1
   	not_used = 'not used'
    a = 'A'
    def f2():             # 함수 2
        b = 'B'
        print(a, b)
        def f3():         # 함수 3
            print(a, b)
        return f3
    return f2
```

- 위와 같이, f1 안에서 f2, f2 안에서 f3가 실행되는 함수가 있다면 아래의 순서로 
  - f1이 호출돼도 외부 변수를 쓰지 않으니 closure 없음
  - f1 안에서 f2가 호출되면, a에 대한 cell object를 만듦
  - f2 안에서 f3가 호출되면, a에 대한 cell object는 f2가 만든 것을 마운트하고 b에 대한 cell object를 만듦
  - not_used 변수는 하위 함수들에서 사용되지 않으니 어디에서도 cell object를 만들지 않음



## id를 통해 같은 객체를 참조하는데 왜 수정은 못 하는가?

- 처음엔 cell object 자체가 value를 가지고 있는 immutable한 객체일 거라고 생각했는데 그렇지 않음

- cell object는 참조 주소값만 가지고 있고, 바깥 scope의 객체와 같은 id를 참조함

- 그런데 재할당이 안 되는 이유는..

  - 단순 할당과 재할당의 내부적인 처리방식에 차이가 있음
    - 단순 할당은 새로운 주소에 값을 넣기만 하면 되는데..
    - 재할당하려면 특정 주소에 찾아가서 읽고, 새로운 값을 그 이름(주소)에 바인딩해야 함
  - 인터프리터 입장에서 보면
    - 좌변에서 x = ... 하니까 x를 로컬 변수로 선언함 -> 더이상 closure를 참조하지 않음
    - 그러고 나서 우변의 x를 보고 로컬에서 x를 찾아봤더니 없네? UnboundError 발생

  - 그 말인즉슨,
    - 좌변이나 우변 중 한 쪽에만 x를 사용하는 건 가능하다.
      - 좌변에만 쓰면 local 변수 x를 새로이 할당할 것이고
      - 우변에만 쓰면 nonlocal 변수 x를 사용해서 연산한 값을 새로운 변수에 할당할 것



## 감상

- 열심히 탐구해서 내부로직을 파고드니 재밌다
- 시간을 꽤 썼는데 코딩실력이랑은 하등 상관 없을 것 같아 좀 걱정이다. 언젠간 도움이 되겠지