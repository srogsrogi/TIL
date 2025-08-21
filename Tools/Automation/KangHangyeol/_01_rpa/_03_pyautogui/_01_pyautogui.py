# pyautogui : 키보드, 마우스 제어
import pyautogui

print(pyautogui.size()) # 모니터사이즈
print(pyautogui.position()) # 커서 위치

pyautogui.mouseInfo() # 실시간 커서위치, 컬러값 등 제공


# 커서 절대좌표로 이동
# pyautogui.moveTo(1700,500, duration = 0.3) # duration에 난수를 넣는다면?

# 현재 커서 위치 기준 상대적으로 이동
# pyautogui.move(-300,-300, duration = 2)

# 클릭
# pyautogui.click(button = 'right') # default = 'left'

# 잠시 대기
import time
# time.sleep(1)
# pyautogui.move(-30,200,duration=1)
# pyautogui.click()

# 키보드 제어
# 메모장 앱 위치에 가서 특정 텍스트 작성해보기

# notepad의 위치 가져오기
notepad_coord_1 = (760,1068)
notepad_coord_2 = (27, 181)
pyautogui.click(*notepad_coord_1, duration = 0.7)
pyautogui.click(*notepad_coord_2)

# 텍스트 작성하기. 한글은 안 됨
pyautogui.write('yz lv u', interval = 0.1)

# 한글입력은 이렇게 클립보드에 복사한 다음 가져오는 형식으로 해야 함
import pyperclip
pyperclip.copy('안녕')
pyautogui.hotkey('ctrl','v')

