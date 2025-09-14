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
- CI/CD
  - github actions
  
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



- VPC / subnet / 보안그룹 관계 / NAT
- DB vs RDS
- ACM(aws ssl 인증 자동화)
- cloudwatching(로깅)
- eb 커스터마이징(.ebextensions | .platform)

```markdown
### 'Advanced Deployment' 커리큘럼 제안


  1단계: 정적 파일 분리 (feat. S3)
     무엇을 하나요?: 현재 EC2 인스턴스에서 애플리케이션과 함께 서빙되고 있는 
  이미지, CSS, JS 파일들을 Amazon S3* 버킷으로 옮깁니다. 그리고 웹페이지가
  S3에 있는 파일들을 바라보도록 HTML을 수정합니다.
     왜 먼저 하나요?*: 애플리케이션(Docker 이미지)의 크기를 줄이고, 배포를 더
  가볍고 빠르게 만듭니다. 이는 이후 진행할 무중단 배포의 유연성을 높여주는
  사전 작업입니다.


  2단계: 무중단 배포 및 롤백 전략 (feat. Nginx)
     무엇을 하나요?: 블루-그린 배포* 개념을 Nginx를 이용해 수동으로
  구현합니다.
      1.  현재 운영 버전(blue) 외에, 새로운 버전(green)의 컨테이너를 동일한
  서버에 함께 띄웁니다.
      2.  Nginx의 upstream 설정을 변경하여 트래픽을 blue에서 green으로
  순식간에 전환합니다.
      3.  green 버전에 문제가 생겼을 경우, Nginx 설정을 다시 blue로 되돌려
  즉시 롤백하는 과정을 실습합니다.
     왜 좋은가요?*: 서비스 중단 없이 배포하는 핵심 원리를 직접 손으로
  구현해보면서 완벽하게 이해할 수 있습니다.


  3단계: 모니터링 및 로깅 (feat. CloudWatch)
     무엇을 하나요?*: 배포된 서비스의 상태를 확인합니다.
      1.  로깅: Nginx 접근 로그와 FastAPI 애플리케이션 로그를 CloudWatch 
  Logs로 전송하도록 설정합니다. "어떤 IP가 몇 시에 접속했나", "어떤 에러가
  발생했나"를 중앙에서 확인합니다.
      2.  모니터링: EC2 인스턴스의 CPU 사용률, 네트워크 트래픽 같은 기본
  지표를 CloudWatch Dashboard로 만듭니다.
      3.  알람: "CPU 사용률이 5분 이상 80%를 넘으면 이메일로 알람 보내기"
  같은 CloudWatch Alarm을 설정합니다.
     왜 좋은가요?*: "배포하고 끝"이 아니라, 운영 중인 서비스의 문제를
  감지하고 원인을 추적하는 '운영'의 첫걸음을 떼게 됩니다.


  4단계: 모든 것의 자동화 (feat. Elastic Beanstalk)
     무엇을 하나요?: 1~3단계에서 수동으로 했던 모든 과정을 Elastic 
  Beanstalk(EB)*이 얼마나 편하게 자동화해주는지 체험합니다. EB 환경을
  생성하고 소스 코드를 업로드하면, EB가 알아서 S3 연동, 블루-그린 배포,
  CloudWatch 로깅 등을 처리해줍니다.
     왜 좋은가요?*: 앞선 단계들 덕분에 EB가 단순한 '마법'이 아니라, 어떤
  원리로 동작하는지 이해하게 됩니다. "왜 관리형 서비스(Managed Service)를
  쓰는가?"에 대한 깊은 통찰을 얻게 됩니다.

  ---


  이 커리큘럼을 완성하면, 수강생들은 단순히 '배포'를 넘어 '안정적인 서비스
  운영'에 대한 깊은 이해를 갖게 될 것입니다. 그리고 님께서는 '실무형 DevOps 
  역량을 갖춘 개발자'라는 강력한 타이틀을 얻게 되실 겁니다. 정말 훌륭한
  계획입니다.
```



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







### 
