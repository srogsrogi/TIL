# 파이썬 공식 이미지를 기반으로 합니다.
# slim 버전은 필요한 최소한의 패키지만 포함하여 이미지 크기가 작습니다.
FROM python:3.11-slim

# 환경변수 설정
# 파이썬이 .pyc 파일을 만들지 않도록 하고(PYTHONDONTWRITEBYTECODE=1),
# print() 등의 출력이 버퍼링 없이 바로 터미널에 표시되도록 합니다(PYTHONUNBUFFERED=1).
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 작업 디렉토리를 /app으로 설정합니다.
# 이후 모든 명령어는 이 디렉토리 안에서 실행됩니다.
WORKDIR /app

# 먼저 requirements.txt 파일을 복사하고,
# pip를 최신 버전으로 업그레이드 한 후, 의존성을 설치합니다.
# 소스 코드를 복사하기 전에 의존성을 먼저 설치하면, 
# 의존성이 변경되지 않았을 경우 Docker가 캐시를 사용하여 빌드 시간을 단축합니다.
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 현재 디렉토리의 모든 파일을 컨테이너의 /app 디렉토리로 복사합니다.
COPY . .

# 컨테이너 외부에서 8000번 포트에 접근할 수 있도록 설정합니다.
# Django 개발 서버의 기본 포트이자, gunicorn을 연결할 포트입니다.
EXPOSE 8000

# 컨테이너가 시작될 때 실행될 기본 명령어입니다.
# gunicorn을 사용하여 Django 애플리케이션을 실행합니다.
# 'nginx_practice.wsgi:application'은 WSGI 설정을 가리키며,
# '--bind 0.0.0.0:8000'은 모든 네트워크 인터페이스의 8000번 포트에서 요청을 받도록 합니다.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "nginx_practice.wsgi:application"]
