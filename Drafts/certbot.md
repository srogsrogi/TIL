# SSL 인증서 발급



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

