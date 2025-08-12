# SSL 인증서 발급

## 주요 개념

- **HTTPS**
  - HTTP에 **보안(SSL/TLS 암호화)**을 추가한 통신 규약
  - 브라우저와 서버 사이의 데이터가 중간에서 **도청·변조되지 않도록 보호**
  - session이 지속되는 동안 유지되는 key를 random seed로 활용하는 암호화 방식

- **SSL 인증서**: 서버가 “진짜 이 도메인 주인”임을 증명하고, 암호화 통신에 필요한 **열쇠**를 제공
  - 발급기관(CA)이 신원 확인 후 발급
  - 브라우저가 ssl인증서를 확인함으로써 보안성을 검증

## 절차

### 1. 보안그룹 443 열기



### 2. nginx 설치

sudo apt update

sudo apt install nginx

sudo apt install certbot python3-certbot-nginx



### 3. uvicorn PORT 변경

nginx가 80포트를 사용해야 하는데 컨테이너 실행될 때 uvicorn이 80포트를 점유하고 있어서 에러가 나는 상황

컨테이너 중지/삭제한 후 다시 run해야 하는데..

포트 설정은 server.py에 있으니

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]으로 바꿔서 이미지 재빌드하고



### 4. 컨테이너 재실행

그 이미지 받은 후에

`docker run -d --name najungh -p 127.0.0.1:8000:8000 myimage`



### 5. ssl인증서 발급

`sudo certbot --nginx -d najungh.site -d www.najungh.site --redirect -m junghyun.na321@gmail.com --agree-tos --no-eff-email`

이거 해주면 ssl인증서 받아질 것



##### 했는데 만약에 안 되면!!



### 6.  리디렉션 설정(nginx conf파일 직접 수정)

- `nginx -t` 로 conf파일 경로 확인

- `sudo nano /etc/nginx/sites-available/default` 해당 파일에 nano 접근

- 설정파일 변경

  ```nginx
  # HTTP 요청 → HTTPS 리디렉션
  server {
      listen 80;
      server_name najungh.site www.najungh.site;
  
      return 301 https://$host$request_uri;
  }
  
  # HTTPS 요청 처리
  server {
      listen 443 ssl;
      server_name najungh.site www.najungh.site;
  
      # SSL 인증서 경로 (Certbot 발급 기준)
      ssl_certificate     /etc/letsencrypt/live/najungh.site/fullchain.pem;
      ssl_certificate_key /etc/letsencrypt/live/najungh.site/privkey.pem;
  
      # SSL 보안 설정 (권장)
      ssl_protocols TLSv1.2 TLSv1.3;
      ssl_ciphers HIGH:!aNULL:!MD5;
  
      location / {
          proxy_pass http://127.0.0.1:8000;  # uvicorn 내부 포트
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }
  }
  ```

- `sudo nginx -t` 문법 검사

- `sudo systemctl restart nginx` nginx 재실행으로 변경사항 적용

- `sudo certbot renew --dry-run` 자동갱신 적용여부 확인

- `curl -I https://najungh.site` 아무 터미널에서나 입력해서 https 연결 확인

