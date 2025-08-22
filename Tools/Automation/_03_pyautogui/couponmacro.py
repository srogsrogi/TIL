import pyautogui
import pyperclip  # 한글 입력 처리
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import time

def load_csv(file_path):
    """CSV 파일 로드"""
    try:
        return pd.read_csv(file_path).iloc[:, 0].tolist()  # 첫 번째 열만 리스트로 반환
    except Exception as e:
        messagebox.showerror("파일 오류", f"'{file_path}' 파일을 읽는 중 문제가 발생했습니다:\n{e}")
        return []

def paste_text(text):
    """텍스트를 클립보드에 복사하고 붙여넣기"""
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")  # Ctrl + V로 붙여넣기

def run_macro():
    """매크로 실행"""
    characters = load_csv("characters.csv")
    coupons = load_csv("coupons.csv")

    if not characters:
        messagebox.showerror("오류", "characters.csv 파일에 유효한 데이터가 없습니다.")
        return
    if not coupons:
        messagebox.showerror("오류", "coupons.csv 파일에 유효한 데이터가 없습니다.")
        return

    messagebox.showinfo("매크로 시작", f"총 {len(characters)}개의 캐릭터와 {len(coupons)}개의 쿠폰 코드에 대해 매크로를 실행합니다.")
    time.sleep(1)  # 사용자 준비 시간

    for char_code in characters:
        for coupon_code in coupons:
            try:
                pyautogui.hotkey("home")
                time.sleep(0.1)
                # 캐릭터 코드 입력
                pyautogui.click(849,558)  # 캐릭터 입력 위치
                paste_text(char_code)  # 한글 입력
                pyautogui.press('tab')

                # 쿠폰 코드 입력
                paste_text(coupon_code)  # 한글 입력
                pyautogui.click(954,685)  # 제출
                time.sleep(0.5)
                pyautogui.click(952,594)  # 확인 누르기
                time.sleep(8)
                pyautogui.click(1050,597)
                time.sleep(2)
                pyautogui.click(956,601)
                time.sleep(0.9)
                pyautogui.hotkey("home")
                # 다음 작업을 위해 잠시 대기
                time.sleep(0.5)
                # 기존 코드 지우기
                pyautogui.click(849,558)  # 캐릭터 입력 위치
                pyautogui.hotkey("ctrl", "a")  # Ctrl + A로 전체 선택
                pyautogui.hotkey("delete")  # 지우기
                pyautogui.press('tab')
                pyautogui.hotkey("ctrl", "a")  # Ctrl + A로 전체 선택
                pyautogui.hotkey("delete")  # 지우기
                time.sleep(0.1)

            except Exception as e:
                messagebox.showerror("매크로 오류", f"매크로 실행 중 문제가 발생했습니다:\n{e}")
                return

    messagebox.showinfo("완료", "모든 캐릭터와 쿠폰 코드 입력을 완료했습니다.")

# GUI 설정
root = tk.Tk()
root.title("캐릭터/쿠폰 매크로 프로그램")
root.geometry("400x200")

tk.Label(root, text="매크로 실행 프로그램", font=("Arial", 14)).pack(pady=10)
tk.Label(root, text="characters.csv 및 coupons.csv 파일을 준비하세요.").pack()

run_button = tk.Button(root, text="매크로 실행", command=run_macro, bg="blue", fg="white", width=20)
run_button.pack(pady=20)

root.mainloop()
