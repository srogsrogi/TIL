# 후위표기법



## 개념

- 연산자를 피연산자 뒤에 표기하는 방법
- 입력이 들어오는 순서대로 처리하도록 하여 컴퓨터가 더 효율적으로 연산할 수 있음



## 코드 구현

### stack을 이용하여 중위표기법 -> 후위표기법 변환

- 알고리즘은 사실상 정해져 있으므로 패턴을 외워두면 됨
- 2자리 이상의 수 처리(공백 활용), 오른쪽 결합성을 가진 연산자(^ 등) 처리, 오류 및 예외처리 등의 알고리즘이 추가될 수 있음

```python
def infix_to_postfix(expression):
    stack = []
    result = []
    
    precedence = {
        '+' : 1,
        '-' : 1,
        '*' : 2,
        '/' : 2
    }

    for token in expression:
        # token이 피연산자
        if token.isalnum():
            result.append(token)
        # 왼쪽 괄호
        elif token == '(':
            stack.append(token)
        # 오른쪽 괄호
        elif token == ')':
            # stack의 top이 (가 될 때까지 모든 연산자를 pop
            # stack이 비어있으면 pop할 수 없음
            while stack and stack[-1] != '(':
                result.append(stack.pop())
            # 반복이 끝난 후 (를 버림
            stack.pop()
        # 연산자
        else:
            # stack top의 연산자 우선순위(isp)와 현재 연산자 우선순위(icp) 비교
            # stack이 비어있지 않고, top이 여는 괄호가 아니고, isp가 icp보다 크거나 같으면 pop
            while (
                stack
                and stack[-1] != '('
                and precedence.get(stack[-1]) >= precedence.get(token)
            ):
                result.append(stack.pop())

            # token이 자기보다 우선순위가 낮은 연산자를 만나면
            # 현재 연산자(token)를 스택에 push
            stack.append(token)
    
    # 모든 token 처리가 끝난 후 stack에 남아 있는 연산자 처리
    while stack:
        result.append(stack.pop())

    return ''.join(result)

# 테스트
expr1 = '(A+B)*C'
expr2 = '(A+B)*(C-D)'
print(infix_to_postfix(expr1))  # "AB+C*"
print(infix_to_postfix(expr2))  # "AB+CD-*"

```



### 후위표기법 연산

- 이것도 알고리즘은 정해져 있음
- 추가로 zero division error 구현 등이 요구될 수도 있음

```python
def evaluate_postfix(expression):
    """
    후위 표기법으로 표현된 수식을 계산하여 결과를 반환하는 함수.

    Args:
        expression (str): 후위 표기법으로 작성된 문자열 (예: "53+2*")

    Returns:
        int or float: 수식의 최종 계산 결과
    """
    stack = []

    # 후위표기된 수식 순회
    for token in expression:
        # token이 숫자인 경우
        if token.isdigit():
            stack.append(int(token))
        # token이 연산자인 경우
        # 먼저 pop한게 꼭 오른쪽으로 가야 함!
        else:
            right = stack.pop()
            left = stack.pop()
            
            if token == '+':
                result = left + right
            elif token == '-':
                result = left + right
            elif token == '*':
                result = left * right
            elif token == '/':
                result = left / right

            # 연산된 값을 stack에 push
            stack.append(result)

    # 반복문이 다 돌고 나면 stack에 값이 1개만 남고, 이게 연산 결과
    return stack.pop()



# --- 실행 코드 ---
# (5 + 3) * 2 를 후위 표기법으로 표현
postfix_expr = "53+2*"
result = evaluate_postfix(postfix_expr)
print(f"'{postfix_expr}'의 계산 결과: {result}")  # '53+2*'의 계산 결과: 16
```

