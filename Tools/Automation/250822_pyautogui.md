# pyautogui



## 개념

### RPA

- Robotic Process Automation
- 사람이 하는 반복적인 컴퓨터 작업을 자동화
- 개념적으로는 범주가 아주 넓음. 주요 하위 주제는..
  - `pyautogui` 등 마우스/키보드 제어
  - `autohotkey`, `pywinauto` 등 OS | App 제어
  - `openpyxl` 등 excel / csv파일 제어
  - 웹 scrapping / crawling
  - 이메일 송수신 자동화
  - 통화 내용 녹음 및 내용 요약



## pyautogui
- python에서 키보드/마우스를 직접 제어할 수 있게 해주는 라이브러리



### 라이브러리 설치

`pip install pyautogui` 

`pip install pillow` : 이미지 처리

`pip install keyboard` : 단축키 감지



### 사용법

#### 종료 조건

- 코드 잘못 짜서 무한루프 걸린다든지 하면 컴퓨터 강제종료밖에 답이 없어질 수도 있으므로 종료조건을 잘 설정해두는 것이 중요

- 마우스 커서를 (0,0) 좌상단 끝으로 이동하면 프로그램 작동이 멈춤
- default True로 설정돼있으므로, 일부러 False로 바꾸지 않으면 아래 코드 작성하지 않아도 작동함

​	`pyautogui.FAILSAFE = True`

- hotkey 입력 등 다른 종료조건을 만드는 것도 가능



#### 정보 확인

- 모니터 사이즈 확인

  `print(pyautogui.size())`

- 현재 커서 위치

  `print(pyautogui.position())`

- 실시간 커서위치, 컬러값 등 제공

  `pyautogui.mouseInfo()`



#### 마우스 제어

- 커서 절대좌표로 이동

​	`pyautogui.moveTo(x, y, duration = 0.3)`

- 현재 커서 위치 기준 상대적으로 이동

​	`pyautogui.move(dx, dy, duration = 2)`

- 클릭

​	`pyautogui.click(button = 'right') # default = 'left'`

잠시 대기

```python
import time
time.sleep(100)
```



#### 키보드 제어
- 텍스트 작성하기(한글 미지원)

​	`pyautogui.write('hi~', interval = 0.1)`

- 한글입력은 이렇게 클립보드에 복사한 다음 가져오는 형식으로 해야 함

  ```python
  import pyperclip
  pyperclip.copy('안녕')
  pyautogui.hotkey('ctrl','v')
  ```




#### 색상 감지

```python
while True:
    current = pyautogui.pixel(x, y)
    # tolerance는 픽셀 rgb 오차 허용 범위. 보통 5~15 권장
    if pyautogui.pixelMatchesColor(x, y, (r,g,b), tolerance=5):
        pyautogui.click(x, y)
```



## 소감

- 이미 게임 쿠폰 입력기, roboflow 이미지 labeling 자동화 등 몇 차례 간단한 매크로 짜서 시간을 아껴본 적이 많음
- 뭔가 반복해야된다 싶으면 다양한 자동화 tool을 먼저 생각하는 습관이 들어서 좋음

- 다음에 배울 자동화 tool은 openpyxl이 될 듯?