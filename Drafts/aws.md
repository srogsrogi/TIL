# AWS, http, django 초안

## 얼추 아는거

- ec2
  - fastapi서버
    - 온갖 ai모델 돌아가는 추론서버(yolo, maskrcnn, 챗봇, twilio openai websocket) 만듦
    - 보통 ec2에서 했지만 로컬서버 만들고 ngrok으로 터널링도 해봄
    - sagemaker나 runpod같은 대안도 알고는 있음
    - 도커 이미지로 배포 - ec2에서 이미지 pull해서 사용
  - mysql db서버
    - 내가 안해서 찾아보고 공부해야할듯
  - 보안그룹 설정
    - 인스턴스별로 보안그룹 할당
    - 보통 접근가능한 외부포트 설정하는 듯?
- eb - 웹서버 통합 관리
  - 브레드스캔소, 태워줘 웹
  - 내가 만든건 아니라 좀 배워야 할 듯
- route53 - DNS설정
  - 원래 acm까지 연결해서 쓰고 있었을 것 같은데.. 과금돼서 지워버리고
  - 직접 let's encrypt ssl인증서 발급했음
- s3 - static파일 관리
  - 로그, 더미데이터, 이미지/영상/음성파일 등 저장
  - 큰 데이터는 직접 저장하는게 아니라 참조할 주소를 저장
- lb
  - 로드밸런싱 켜노니까 최소 2개 서버를 준비해놔서 프리티어 과금됨.. 단일인스턴스로 돌렸음
  - scale out방식 사용
  - alb | nlb

- 환경변수 관리
  - .env
  - 컨테이너 실행시 CLI로 직접 변수 하나하나 등록하는 것도 가능
  - api key, debug=, PORT 등
- requirements
  - 그냥 다 최신버전 깔리게 버전 명시 안했는데, 어떤 라이브러리만 업데이트되고 그러면 꼬일 수 있으니까 적어도 배포할 최종 버전이라도 버전 명시해서 기록하는게 좋을 듯? 알아봐야 함

- CLI / mobaxterm
  - ssh 접속에 대한 개념 필요
  - mobaxterm 추가기능같은거, 아니면 그냥 cmd상에서도 하는 법 좀 더 알아도 좋을듯
- CI/CD(github actions)
  - 예진이꺼 보고 정리

## 잘 모르는 키워드

- uvicorn, gunicorn
- sync async await...
- nginx
  - reverse proxy
- 내외부 PORT 설정
- http 프로토콜?
- fastapi
- ASGI WSGI

- rest api | restful
- AWS IAM
- 로깅



## GPT 추천

- VPC / subnet / 보안그룹 관계 / NAT
- DB vs RDS
- ACM(aws ssl 인증 자동화)
- cloudwatching(로깅)
- eb 커스터마이징(.ebextensions | .platform)

