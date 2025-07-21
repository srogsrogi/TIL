# OpenAI Realtime API

- 실시간 음성 스트리밍 기반의 대화형 API

- STT + GPT + TTS가 통합된 스트리밍 구조

- realtime api는 매달 무료로 주는 크레딧으로는 사용 불가. 직접 과금한 크레딧 필요

  

## 공식 API 문서

https://platform.openai.com/docs/guides/realtime



## 활용한 프로젝트

- 호출형 공공 교통 서비스(DRT) 프로젝트 중 유선전화로 연결되는 음성 챗봇 서버를 구현

- Twilio 유선 전화를 통해 WebSocket 서버와 연결해 OpenAI Realtime API로 실시간 대화 처리

- https://github.com/srogsrogi/Tajo-AI-Hackaton-2025

  

## 주요 구성 요소

### 서버간 연결

- 웹 앱 등에서 클라이언트와 직접 연결할 때는 WebRTC 사용 권장
  - 네트워크 상태가 좋지 않은 경우에도 비교적 안정적으로 미디어 전송 가능
- 서버간 통신이 목적인 경우 websockets로 연결(프로젝트에서는 이걸 사용함)

### 전송 메시지 종류

- voice : [alloy`, `ash`, `ballad`, `coral`, `echo`, `sage`, `shimmer]
-  JSON 이벤트
- base64로 인코딩된 오디오

## 작동 방식

- WebRTC 또는 Websocket으로 session객체를 만들어 시작
- 각 세션은 최대 30분 지속
- session.update 이벤트로 실시간 세션 상태를 업데이트시키는 방식으로 동작
- voice 속성을 제외하고는 대부분의 세션 속성을 언제든지 업데이트할 수 있음

- 음성 감지(VAD), 함수 호출, 전사 모드 등 지원하니 API 문서 참고



## 감상

- session객체 다루는게 익숙하지 않아서 처음에는 애를 좀 먹었다.
- 비슷한 방식으로 동작하는 api들 써보다 보면 금방 잘 쓸 듯.
- 직접 STT-LLM-TTS모델을 만들었을 때는 (물론 아무 최적화도 안 했지만..) 대답 한 번에 20초 이상이 소요됐는데, 단일 api가 모든 과정을 한 번에 처리해주면서도 속도, 성능, 가격 모두 압도적으로 좋아서 놀랐다.
