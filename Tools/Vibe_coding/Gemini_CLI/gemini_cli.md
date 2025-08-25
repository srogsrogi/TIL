# Gemini-CLI

- CLI 기반 코딩 어시스턴트



## 사전 준비

- vscode와 함께 사용
- Node.js 설치
- Gemini CLI Companion extension 설치

- `npm install –g @google/gemini-cli`



## 실행

`gemini`

`gemini -m "gemini-1.5-flash"` : 버전 지정 실행



## 명령어

- `/compress` : 지금까지 대화내용 압축(토큰 절약)
- `/chat`
  - `/chat save <tag>` : 대화내용 저장. 안 하고 끄면 다 날아감
  - `/chat list`
  - `/chat resume <tag>`
  - `/chat delete <tag>`



##### 로그인하고 파일 수정 권한 주고 프롬프트 주면 코딩 다 해줌..