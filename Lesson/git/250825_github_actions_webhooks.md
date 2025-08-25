# Github Actions | Webhooks



## Warm-up

##### 프로젝트를 하고 있는데, 팀원이 코드를 푸시하면 알림을 받고 싶어!

##### 깃허브 리포지토리와 협업 tool을 연동해보자.



## 이후 수업 진행

### 이론

- 수업자료 : `"C:\Users\SSAFY\AppData\Local\workspaces\TIL\Git\250825_actions_webhook.md"`

- Actions와 Webhook에 대한 간략한 설명
  - 각 개념/기능의 정의 및 활용법
  - Incoming / Outgoin Webhooks 구분
  - Repo secret 사용의 필요성 등



### 실습

- Github repo에 push 이벤트가 발생할 경우 Mattermost의 특정 채널로 알림이 가도록 하는 Incoming Webhook 설정 및 테스트
  - MM Webhook URL 발급
  - yaml 파일 작성(GPT)
  - Github Actions에서 workflow 추가/확인
  - commit - push - 알림 오는지 확인