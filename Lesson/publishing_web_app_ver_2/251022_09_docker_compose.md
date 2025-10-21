# Docker compose



## 선수 지식

- 가상화 기술(VM, Container)의 개념
- AWS EC2, Docker 사용법 기초
- 웹 서비스 시스템 아키텍쳐에 대한 이해



## 학습 목표

- 배포 인프라 구축에서 명령형|선언형 패러다임의 차이를 예시와 함께 설명할 수 있다.
- Docker compose 기능을 활용한 선언형 인프라 구축 과정을 설명할 수 있다.

- compose용 `.yml`파일의 구조와 구성 요소에 대해 설명할 수 있다.



## Warm-up

- 지금까지 여러분이 `docker run` 명령어로 컨테이너를 실행할 때마다 명령어를 정확히 어떻게 입력해야 하는지 헷갈리셨을텐데요.
- 매번 `docker run -d -p --env-file ./wisheasy/.env 8000:8000` 같은 긴 명령어를 똑같이 입력하는 것은 비효율적이고 재현성이 떨어집니다.
- 실제 서비스를 구현하기 위해 여러 개의 Container를 실행해야 하는 경우, Container 간 관계 설정 등을 위해 훨씬 더 긴 명령어들을 연속으로 입력해야 합니다.
- 그러한 비효율성을 없애고, 코드로서 인프라 상태를 유지(IaC)하는 방법을 배워 봅시다.



## 이론

### 명령형 | 선언형 패러다임

| 구분          | 명령형(Imperative)       | 선언형(Declarative)                                 |
| ------------- | ------------------------ | --------------------------------------------------- |
| **핵심 철학** | “지금 이걸 해라.”        | 이 상태가 되게 해라.                                |
| **관점**      | 과정 중심                | 결과 중심                                           |
| **상태 관리** | 사용자가 직접 추적       | 시스템이 현재 상태와 목표 상태를 비교해서 자동 조정 |
| **변경 방식** | 수동 업데이트(명령 반복) | 상태 동기화(선언만 하면 자동 반영)                  |

- `Docker run`은 명령어 입력 시점에 한 번만 실행되는, 대표적인 명령형 기능이었습니다.
- 오늘 배울 `Docker compose`는 선언형 기능에 속합니다.



### Docker compose

- 여러 개의 Container를 묶어 하나의 앱으로 배포할 수 있게 해주는 Docker의 기능
- `.yml` 파일을 통해 Container 환경을 설정하고, 동시에 Container를 실행하는 명령
  - 명령어 예시 : `docker compose --file docker-compose.prod.yml up -d`
- `.yml` 파일에는 다음과 같은 요소들이 포함됨
  - 개별 Container 설정
    - 실행하는데 사용할 Image 이름
    - 실행할 Container 이름
    - 참조할 환경 변수
    - 재실행 조건 등
  - Container 간 연결 설정
    - 열어둘 PORT 번호
    - Container 간 의존성
    - 호스트 엔진 내부에서 공유할 네트워크
    - 별도 저장 공간(Volumes)



#### 서버 환경에서 compose 사용시 주의사항

- Docker compose는 `ubuntu`의 앱 관리자인 `apt`에 배포되어 있는 `docker.io` 버전에서는 지원하지 않는 기능입니다.

  - `ubuntu` 환경에서 compose 기능을 실행하기 위해서는

    - `docker.io`에 `compose` 모듈을 따로 설치하거나
    - `docker-ce` 버전을 설치해야 합니다.

  - 되도록 `docker-ce` 버전 설치 및 사용을 권합니다.

    - 별도의 docker 앱 저장소를 등록하고 key를 발급받는 등 몇 가지 절차를 거쳐 설치할 수 있습니다.
    - 설치법은 GPT가 잘 알려주니까 강의에서는 생략합니다.

    

### Volume

#### 개념

- 컨테이너 밖(호스트 엔진 안)에 있는 저장 공간
- 컨테이너가 꺼져도 데이터가 사라지지 않도록 보존하는 방법

#### 필요성

- Container는 앱 재배포 또는 auto-scaling 과정에서 생성되고 삭제되기를 반복합니다.
- 그런데 Container는 이미지를 기반으로 생성되기 때문에, 서비스 운영 과정에서 생겨난 데이터들은 컨테이너가 사라질 때 같이 삭제됩니다.
- Nginx 설정 파일, DB에 저장된 데이터, 기능 실행 로그 등이 Container가 재실행될 때마다 초기화된다면 서비스가 유지될 수 없습니다.
- 그래서 컨테이너 밖에서, Docker가 관리하는 `Volume`이라는 공간을 두어 영속성이 필요한 데이터를 저장하거나 불러와서 사용합니다.



## 실습

### compose 설정 파일 읽어 보기

- 참여하고 계신 wisheasy 프로젝트에서 활용하는 compose 설정 파일입니다.
- 처음부터 한 줄 한 줄 자세히 보려고 하지 말고, Top-Down 방식으로 구조를 이해하세요.
  - services 안에 세 개의 service(db, web, nginx)가 있습니다.
  - service 안에 각 service에 대한 설정값이 있습니다.
  - 맨 아래 networks, volumes는 모든 service가 공유하는 객체입니다.

```yaml
services: # service는 각각의 container를 칭함. 이 파일에서는 db, web, nginx
  db: # 첫 번째 Container : MySQL DB
    image: mysql:8.0 # Oracle에서 DockerHub에 배포한 MySQL 공식 Image
    container_name: mysql_db # Container 이름
    restart: always # Container 재실행 조건
    env_file: .env # 참조할 env 파일 경로
    environment: # .env 파일 외에 추가로 주입할 환경 변수
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    volumes: # volume(호스트 엔진의 저장 공간) 경로. DB 데이터 값 및 설정 파일 저장
      - mysql_data:/var/lib/mysql
      - ./mysql/conf.d:/etc/mysql/conf.d:ro 
    networks: [appnet] # service들이 내부적으로 통신할 네트워크 이름
    healthcheck: # Container 실행시 실행할 healthcheck 정의
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "${MYSQL_USER}", "-p${MYSQL_PASSWORD}"]
      interval: 5s
      timeout: 5s
      retries: 90

  web: # 두 번째 Container : Django Web 서버
    image: "${DOCKERHUB_IMAGE}:${IMAGE_TAG}"
    container_name: wisheasy_web
    restart: always
    env_file: .env
    environment:
      SECRET_KEY: ${DJANGO_SECRET_KEY}
      DJANGO_DEBUG: ${DJANGO_DEBUG}
      MYSQL_HOST: ${DB_HOST:-db}
      MYSQL_PORT: ${DB_PORT:-3306}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_DB: ${MYSQL_DATABASE}
      DJANGO_SETTINGS_MODULE: config.settings.prod
      GOOGLE_CLIENT_ID: ${GOOGLE_CLIENT_ID}
      GOOGLE_CLIENT_SECRET: ${GOOGLE_CLIENT_SECRET}
      SITE_DOMAIN: ${SITE_DOMAIN}
    volumes: # volume 경로. 정적 파일, 서버 로그, 기타 앱 데이터
      - ./staticfiles:/app/staticfiles
      - ./logs:/app/logs
      - app_data:/data

    networks: [appnet]
    expose: # 네트워크 내부에서의 노출할 PORT(서버 외부로의 노출을 의미하지는 않음)
      - "8000"
    depends_on: # 실행 조건 : 다른 service(DB) 실행 대기
      db:
        condition: service_healthy
    command: > # 이 컨테이너 실행시 입력할 명령어(gunicorn으로 서버 실행)
      sh -lc "
      gunicorn config.wsgi:application
      --bind 0.0.0.0:8000
      --access-logfile /app/logs/gunicorn_access.log
      --error-logfile /app/logs/gunicorn_error.log
      --log-level debug
      "

  nginx: # 세 번째 Container : Nginx
    image: nginx:1.27-alpine # Nginx 공식 이미지
    container_name: nginx_edge
    restart: always
    depends_on:
      - web
    ports: # 서버 외부로 열려 있는 PORT. expose와의 구분 중요!
      - "80:80"
      - "443:443"
    volumes: # volume 경로. Nginx 설정 파일, SSL 인증서 경로, 정적 파일 경로
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
      - ./staticfiles:/app/staticfiles:ro
    networks: [appnet]

# 위에서 정의된 Service(=Container)들이 사용할 network 정의
networks:
  appnet:
    external: true # appnet은 compose하기 전에 외부에서 만들어짐

# 위에서 정의된 Service(=Container)들이 공통적으로 사용할 volumes 정의
volumes:
  mysql_data: # DB 데이터
  app_data: # Django 앱 데이터
```



## Wrap-up Quiz

- Docker에서 **run**을 여러 번 하는 대신 **compose**로 컨테이너를 실행하는 이유는 무엇인가요?

- `compose.yml` 파일에 **volumes** 필드가 없다면, DB 컨테이너가 재생성될 때 어떤 문제가 생길까요?
- CI-CD workflow에 Docker compose 기능을 통합하는 방법에 대해 생각해봅시다.



## 강의 마무리

- 마지막 두 번의 강의에서는 실습을 대부분 생략하고 개념적인 부분에 조금 더 집중했습니다.
  - 간단한 과정이라도 직접 해보면 이해의 깊이도 깊어지고 기억에 오래 남습니다.
  - CI-CD와 선언형 인프라 구축은 현대적 앱 개발의 표준적 방법론들이니 더 신경써서 복습하며 이해하시고,
  - 이후에 프로젝트를 하실 때 교안을 다시 보면서 CI-CD workflow 구축과 compose 활용에 도전해보시기 바랍니다.
- 지금까지 총 9차시에 걸쳐 현대적인 DevOps의 핵심적인 방법론들을 전부 훑어보셨습니다.
  - 어느 분야의 개발자로 일하게 되든지, 내가 개발한 코드가 어떤 과정을 거쳐 실행되는지에 대한 감각은 반드시 필요합니다.
  - 지금 하고 계신 프로젝트도, 앞으로 하실 프로젝트들도 사용하는 도구는 바뀔지언정 큰 흐름은 변하지 않으니 배운 내용을 기반으로 프로젝트 및 서비스의 구조를 이해하는 개발자가 됩시다.
- 다음 시간에는 여태 배운 내용들을 프로젝트에서 실제로 적용하는 방법과 앞으로의 학습 방향성을 안내해주는 시간을 가지며 과정을 마무리하겠습니다. 수고하셨습니다.