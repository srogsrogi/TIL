# 다뤄볼만한 주제

## Web

- fastapi

  - 온갖 ai모델 돌아가는 추론서버(yolo, maskrcnn, 챗봇, twilio openai websocket) 만듦
  - 보통 ec2에서 했지만 로컬서버 만들고 ngrok으로 터널링도 해봄
  - sagemaker나 runpod같은 대안도 알고는 있음

- eb - 웹서버 통합 관리

  - 브레드스캔소, 태워줘 웹
  - alb / nlb
  
- route53 - DNS설정

  - 원래 acm까지 연결해서 쓰고 있었을 것 같은데.. 과금돼서 지워버리고
  - 직접 let's encrypt ssl인증서 발급했음

- s3 - static파일 관리

  - 로그, 더미데이터, 이미지/영상/음성파일 등 저장
  - 큰 데이터는 직접 저장하는게 아니라 참조할 주소를 저장

- 환경변수 관리

  - .env
  - 컨테이너 실행시 CLI로 직접 변수 하나하나 등록하는 것도 가능
  - docker run할 때 `--env-file` 옵션
  - api key, debug=, PORT 등

- CI/CD(github actions)

  - 예진이꺼 보고 정리

- HTML, CSS

  - iframe 태그, Youtube Embed 주소 연결

- JavaScript

- React / Vue

- Django



- sync async
- 내외부 PORT 설정
- rest api | restful
- serverless
- logging / monitoring
- CORS

### 

- VPC / subnet / 보안그룹 관계 / NAT
- DB vs RDS
- ACM(aws ssl 인증 자동화)
- cloudwatching(로깅)
- eb 커스터마이징(.ebextensions | .platform)



## NLP / LLM

- transformer
- tokenizing
- benchmark
- RAG
- prompt engineering

- hugging face
- langchain



## RPA

- 매크로
  - pyautogui
  - openpyxl
- scrapping / crawling



## DB

- mysql db

  - ec2에 연결 or AWS 서비스 이용

- NoSQL
- VectorDB



## Git

- branch

  - HEAD
  - PR / Merge
  - ff merge / non-ff merge
  - fetch




## API

- Naver map
- 번역
- OpenWeatherMap
- OpenAI
  - llm models
  - Whisper
  - Realtime

- 결제
  - VAN / PG

- 데이터 포털



## Integration

- webhook
  - github
  - slack
  - discord
