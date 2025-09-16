# Github Actions | Webhook



## 개념

### Github Actions

- Github 저장소 안에서 자동화된 작업(workflow) 파이프라인을 실행할 수 있는 기능
- 이벤트(예: 코드 푸시, PR 생성, 이슈 등록 등)를 **Trigger**로 잡아 자동 실행
- Workflow(`.github/workflows/*.yml`) 파일을 통해 실행
- Webhook 외에도 CI/CD를 위해 주로 사용하는 기능



### Webhook

- 이벤트가 발생했을 때, 지정된 URL로 HTTP POST 요청을 보내는 방식
- 서버나 서비스(Github)가 이벤트를 다른 시스템에 알려주는 용도
- Slack, Mattermost, Discord 등 대부분의 협업 툴이 앱 내에서 Webhook URL을 제공

- Webhook의 두 가지 방향

  - `Incoming Webhook` : 외부 서비스에서 POST요청이 들어오는 경우
  - `Outgoing Webhook` : 앱에서 외부 서버로 요청을 내보내는 경우

  

## 실습

- 알림이 오기를 원하는 App에서 Webhook URL 발급

- 아래 예시와 같이 `.github/workflows/xx.yml` 파일 작성

  ```yaml
  name: Notify Mattermost on Push
  
  on:
    push:
      branches: ["**"]
  
  jobs:
    notify:
      runs-on: ubuntu-latest
  
      steps:
        - name: Build payload JSON
          env:
            GITHUB_EVENT: ${{ toJson(github.event) }}
            REPO:   ${{ github.repository }}
            BRANCH: ${{ github.ref_name }}
            ACTOR:  ${{ github.actor }}
          run: |
            node -e '
              const evt = JSON.parse(process.env.GITHUB_EVENT || "{}");
              const commits = (evt.commits||[]).map(c => `- ${c.message} (${c.id.slice(0,7)})`).join("\n") || "- (no commit messages)";
              const text =
                `*${process.env.REPO}*에 push event 발생\n` +
                `브랜치: \`${process.env.BRANCH}\`\n작성자: ${process.env.ACTOR}\n\n` +
                commits;
              require("fs").writeFileSync("payload.json", JSON.stringify({ text }));
            '
  
        - name: Send to Mattermost
          run: |
            curl -sS -X POST \
              -H 'Content-Type: application/json' \
              --data-binary @payload.json \
              'https://meeting.ssafy.com/hooks/4qcxaequ5ido7b4yjbxog1e3fo' \
              -w '\nHTTP %{http_code}\n'
  ```

- Github repo - Settings - Webhooks에서 Webhook 추가

  - Payload URL에 발급받은 webhook URL 입력
  - Content Type은 대부분 JSON 사용
  - Trigger 설정 커스터마이징



## 주의사항

- Webhook URL이 공개되어 있으면 누구나 그 URL로 요청을 넣을 수 있기 때문에 공격당할 수 있음
- 실제 서비스 배포할 경우 반드시 Github Settings의 `Secrets and Variables`에서 `repository secret`에 Webhook URL을 등록하여 사용할 것
- 실습 후 Webhook URL 폐기할 거라 실습할 때는 적용하지 않았음