import pyautogui
import time
import keyboard  # 단축키 감지를 위한 라이브러리

# ✅ 6번 클릭할 좌표와 지연 시간 설정 (튜플 형식: (x, y, delay))
click_positions = [
    (1882, 507, 0.5),  # 첫 번째 클릭 (좌표: (1882, 507), 지연 시간: 0.5초)
    (832, 566, 0.5),   # 두 번째 클릭 (좌표: (832, 566), 지연 시간: 0.5초)
    (1102, 598, 1.6),  # 세 번째 클릭 (좌표: (1102, 598), 지연 시간: 1.6초)
    (507, 406, 0.6),   # 네 번째 클릭 (좌표: (507, 406), 지연 시간: 0.6초)
    (536, 300, 0.6),   # 다섯 번째 클릭 (좌표: (536, 300), 지연 시간: 0.6초)
    (1024, 135, 0.6)   # 여섯 번째 클릭 (좌표: (1024, 135), 지연 시간: 0.6초)
]

# ✅ 반복 횟수 설정
repeat_count = int(input("💡 반복 횟수를 입력하세요: "))

# ✅ 매크로 시작
print(f"🚀 매크로 시작: 3초 후 실행됩니다. | 총 반복 횟수: {repeat_count}회")
print("💡 'q'를 눌러 매크로를 중단할 수 있습니다.")
time.sleep(3)  # 시작 전에 3초 대기

# ✅ 반복 실행
try:
    for r in range(repeat_count):
        print(f"\n🔁 {r+1}번째 반복 시작")

        for i, (x, y, delay) in enumerate(click_positions):
            # 중단 키 확인
            if keyboard.is_pressed('q'):
                print("\n❌ 매크로가 중단되었습니다!")
                raise KeyboardInterrupt  # 안전하게 종료

            print(f"👉 {i+1}번째 위치 클릭: ({x}, {y}) | 지연 시간: {delay}초")
            pyautogui.click(x, y)  # 지정된 위치 클릭
            time.sleep(delay)      # 클릭 후 지정된 지연 시간 대기

        print(f"✅ {r+1}번째 반복 완료!")

    print("✅ 모든 클릭 작업 완료!")

except KeyboardInterrupt:
    print("\n✅ 안전하게 종료되었습니다!")