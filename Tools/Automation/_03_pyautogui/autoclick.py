import pyautogui
import time
import keyboard

# ✅ 6번 클릭할 좌표와 지연 시간 설정 (튜플 형식: (x, y, delay))
click_positions = [
    (898, 130, 0.8) # 여섯 번째 클릭 (좌표: (1100, 1200), 지연 시간: 1.2초)
]

# ✅ 반복 횟수 설정
repeat_count = int(input("💡 반복 횟수를 입력하세요: "))

# ✅ 매크로 시작
print(f"🚀 매크로 시작: 3초 후 실행됩니다. | 총 반복 횟수: {repeat_count}회")
time.sleep(3)  # 시작 전에 3초 대기

try:
    for r in range(repeat_count):
        print(f"\n🔁 {r+1}번째 반복 시작")

        for i, (x, y, delay) in enumerate(click_positions):
            if keyboard.is_pressed('q'):  # 중단 키 확인
                print("\n❌ 매크로가 중단되었습니다!")
                raise KeyboardInterrupt  # 안전한 종료

            print(f"👉 {i+1}번째 위치 클릭: ({x}, {y}) | 지연 시간: {delay}초")
            pyautogui.click(x, y)  # 지정된 위치 클릭
            time.sleep(delay)      # 클릭 후 지정된 지연 시간 대기

        print(f"✅ {r+1}번째 반복 완료!")

    print("✅ 모든 클릭 작업 완료!")

except KeyboardInterrupt:
    print("\n✅ 안전하게 종료되었습니다!")

