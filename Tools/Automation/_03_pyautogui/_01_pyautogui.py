# pyautogui : 키보드, 마우스 제어
import pyautogui

# print(pyautogui.size()) # 모니터사이즈
# print(pyautogui.position()) # 커서 위치

pyautogui.mouseInfo() # 실시간 커서위치, 컬러값 등 제공


# 커서 절대좌표로 이동
pyautogui.moveTo(1700,500, duration = 0.3) # duration에 난수를 넣는다면?
pyautogui.moveTo(130,500, duration = 0.3)
pyautogui.moveTo(0,0, duration = 0.3)

# 현재 커서 위치 기준 상대적으로 이동
pyautogui.move(-300,-300, duration = 2)

# 클릭
pyautogui.click(button = 'right') # default = 'left'

# 잠시 대기
import time
time.sleep(1)
# pyautogui.move(-30,200,duration=1)
# pyautogui.click()

# 키보드 제어
# 메모장 앱 위치에 가서 특정 텍스트 작성해보기

# notepad의 위치 가져오기
# notepad_coord_1 = (760,1068)
# notepad_coord_2 = (27, 181)
# pyautogui.click(*notepad_coord_1, duration = 0.7)
# pyautogui.click(*notepad_coord_2)

# 텍스트 작성하기. 한글은 안 됨
pyautogui.write('hi~', interval = 0.1)

# 한글입력은 이렇게 클립보드에 복사한 다음 가져오는 형식으로 해야 함
import pyperclip
pyperclip.copy('안녕')
pyautogui.hotkey('ctrl','v')



# 커서 대기하다가 알림창 뜨자마자 확인 누르기
x, y = 102, 785   # 확인 버튼 좌표
target_color = (0, 86, 225)  # 파란색 (알림창 뜬 상태의 색)

print("알림창 감시 시작... (Ctrl+C로 종료)")

while True:
    current = pyautogui.pixel(x, y)

    # tolerance는 픽셀 rgb 오차 허용 범위. 보통 5~15 권장
    if pyautogui.pixelMatchesColor(x, y, target_color, tolerance=5):
        pyautogui.click(x, y)
        print("알림창 감지 → 확인 버튼 클릭!")
        break
    time.sleep(0.5)