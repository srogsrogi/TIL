# 제어문

- 조건문, 반복문 기초문법 배움
- 수료 조건인 알고리즘 IM시험이 주로 제어문을 통한 2차원 리스트 조작을 평가
- 명확하게 알지 못했던 내용들만 정리

- 추가로 map, zip, enumerate, for-else문 연습했음

  

## for문과 while문

- for문은 횟수의 관점에서 반복문을 작성
- while문은 종료될 때까지의 과정이 중요한 경우에 작성
- 모든 for문은 while문으로 바꿀 수 있지만 역은 성립하지 않음



## iterable

- 반복 가능한 객체
- for 반복문에서 in 뒤에 오는 객체는 반드시 이터러블이어야 함
- 모든 시퀀스는 이터러블
- set, dict, map/zip/filter객체 등은 이터러블이지만 시퀀스는 아님



## flag를 iterable의 index로 동시에 활용

- 처음 써보는 방식이라 남겨둠..

```python
count = 0

while count < len(food_list):
    food = food_list[count]

    if food['이름'] == '토마토':
        food['종류'] = '과일'

    if food['이름'] == '자장면':
        print('자장면엔 고춧가루지')

    print(f'{food['이름']} 은/는 {food['종류']}이다.')
    count += 1
print(food_list)
```





## 질문/답변

- Q1. range() 안에 int 말고 다른 자료형이 올 수가 있나?
  - ㄴㄴ. 무조건 int만 됨
