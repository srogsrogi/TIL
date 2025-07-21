# Auto Hotkey

- open git bash here / open vscode here 마우스로 추가옵션 들어가서 클릭하기 귀찮은데..

- 커스텀 단축키를 만들어보자!

https://www.autohotkey.com/

- 프로그램 설치 필수
  - 단축키 커스터마이징을 위한 script(.ahk)를 만들 수 있음
  - .ahk 파일의 실행기

![image-20250721125836451](C:\Users\SSAFY\AppData\Roaming\Typora\typora-user-images\image-20250721125836451.png)

- `New script` -> `Edit` 들어가서 코드 쓰고 저장

  - 되도록이면 윈도우에서 원래 제공하는 단축키들은 피해서 만드는게 좋음

- .ahk파일 실행시 작동. 이것도 자동화하려면 시작프로그램에 넣어주시고..

- 여러 기능 넣을 수 있을텐데.. 내가 만든 건 윈도우 탐색기에서 단축키를 누르면 그 위치에서 git bash나 vscode를 실행해주는 프로그램. 사용한 코드는 아래 참고

  ```
  #Requires AutoHotkey v2.0
  #SingleInstance Force
  
  !+g:: {  ; Alt + Shift + G → Git Bash
      hwnd := WinActive("ahk_class CabinetWClass")
      if !hwnd {
          MsgBox "탐색기 창이 활성화되어 있지 않습니다."
          return
      }
  
      for win in ComObject("Shell.Application").Windows {
          if (win.HWND = hwnd) {
              path := win.Document.Folder.Self.Path
              Run '"C:\Program Files\Git\git-bash.exe"', path
              return
          }
      }
  
      MsgBox "탐색기 경로를 찾을 수 없습니다."
  }
  
  #Requires AutoHotkey v2.0
  #SingleInstance Force
  
  !+v:: {  ; Alt + Shift + V → VS Code 열기
      hwnd := WinActive("ahk_class CabinetWClass")
      if !hwnd {
          MsgBox "탐색기 창이 활성화되어 있지 않습니다."
          return
      }
  
      for win in ComObject("Shell.Application").Windows {
          if (win.HWND = hwnd) {
              path := win.Document.Folder.Self.Path
              Run '"C:\Users\SSAFY\AppData\Local\Programs\Microsoft VS Code\Code.exe" .', path
              return
          }
      }
  
      MsgBox "탐색기 경로를 찾을 수 없습니다."
  }
  ```

  

## 후기

- playdata 부트캠프 때도 IDE 처음 써보면서 파이참에서 코드 스니펫 기능 스스로 생각해내서 커스텀 단축키 만들고 습관 들여서 잘 활용하고 있었는데
- ssafy에서도 오래오래 쓸 수 있는 기능 하나 만들어서 좋다. 다방면으로 활용도도 클 듯