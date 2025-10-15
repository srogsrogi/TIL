# SSL 인증서 발급

## HTTP | HTTPS

- http
  - 서버-클라이언트가 통신할 때, 데이터를 원형으로 보냄(중간에서 탈취 가능)

- https

  - session이 새로 생길 때마다 서버와 클라이언트가 난수를 교환하여 그걸 기반으로 대칭 key 생성

  - key(random seed와 비슷한 역할)를 바탕으로 데이터를 암호화
  - key가 없으면 복호화 불가



## 절차

### 1. AWS 보안 그룹 PORT 열기

- 443(https)
- 80(http)
  - 어차피 https로 리디렉션하더라도 입구가 되는 80 PORT는 계속 필요함

### 2. nginx 설치

- `sudo apt update`

- `sudo apt install nginx`

- `sudo apt install certbot python3-certbot-nginx`



### 3. uvicorn PORT 변경

- nginx가 80포트를 사용해야 하는데 컨테이너 실행될 때 uvicorn이 80포트를 점유하고 있으면 충돌 발생

- 포트 설정은 dockerfile에 있으니 80이 아닌 PORT를 사용하도록 dockerfile 수정

- `CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]` 



### 4. 컨테이너 재실행

- docker image 재빌드, push, pull한 후 바뀐 포트로 실행

- `docker run -d -p 8000:8000 myimage`



### 5. ssl인증서 발급

- `sudo certbot --nginx -d najungh.site -d www.najungh.site --redirect`



##### 했는데 만약에 안 되면!!

##### `nano`라는, linux계열 os에 있는 내장 파일 편집기를 통해 설정 파일을 직접 수정해줘야 함

### 6.  ssl인증서 참조, 리디렉션 설정(nginx conf파일 직접 수정)

- `nginx -t` 로 `.conf`파일 경로 확인
- `sudo nano /etc/nginx/sites-available/default` 해당 파일에 nano 접근

- `default`가 아닌 `.conf`파일에 접근해야 하는 경우도 있음. 설정하기 나름

- 설정파일 변경(예시)

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

- `sudo nginx -t` 

  - 문법 검사

- `sudo systemctl restart nginx` 

  - nginx 재실행으로 변경사항 적용
  - 이미 nginx가 작동중인 경우 reload도 가능

- `sudo certbot renew --dry-run`

  - 자동갱신 적용여부 확인

- `curl -I https://najungh.site`
  
  - 아무 터미널에서나 입력해서 https 연결 확인
