# SSL 인증서



## 들어가기 전에..

- 전에 만든 개인 사이트는 http로만 접속 가능
- 보안이 좋은 https로 접속할 수 있도록 ssl인증서를 받고
- http로 접속하더라도 https로 자동으로 연결되도록 설정해줄 것



##### 실습 내용

1. EC2 인스턴스에 연결되어 있는 보안 그룹 PORT 443(https) 열기
   - 22(ssh)와 80(http)는 예~전에 열어 놓음
2. uvicorn이 사용하는 PORT 변경
   - dockerfile에 정의되어 있는 uvicorn PORT가 80으로 되어 있었음
   - nginx가 설치되어 PORT 80을 사용할 경우 충돌이 나기 때문에
   - uvicorn PORT는 8000으로 변경
   - `CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]`
3. docker 이미지 build -> push -> ec2에서 pull -> container 실행
   - `docker run -d -p 8000:8000 <image_name>`

4. ec2에 nginx와 certbot 설치
   - `apt update`
   - `apt install nginx`
   - `apt install certbot python3-certbot-nginx`

5. ssl 인증서 발급

   - `certbot --nginx -d najungh.site -d www.najungh.site --redirect`
     - 이메일 작성과 약관 동의 등을 추가로 해줘야 함
     - nginx 설정파일이 `defaults`와 `.conf` 두 종류가 있고, OS 버전별로 작동방식이 조금씩 다를 수 있음
     - 명령어로 ssl인증서를 받을 때 certbot이 설정파일을 수정하는데, 중복 코드가 생기거나 참조하지 않는 파일에 작성하거나 하는 등 오류가 생길 수 있음
     - 만약 문제가 생기면 설정파일 2개를 `nano` 편집기로 접근하여 직접 확인하고 GPT와 함께 수정할 것
   - `nginx -t` 
     - 현재 상태에서 nginx가 작동 가능할지 테스트
     - 설정파일 문법을 체크해줌

   - `systemctl restart nginx`
     - reload도 가능

   - `systemctl certbot renew --dry-run`
     - 자동갱신 적용여부 확인



##### 실습 중 발생했던 오류

- 기존에 실행되고 있던 nginx 프로세스가 꺼지지 않은 상태에서, 80 PORT를 사용하고 있음
- `nginx reload`하려고 하면 꺼져있다고 하고, `nginx -t` 테스트는 잘 되는 상황
- `nginx start`를 여러 번 해서 프로세스는 여러 개가 연달아 켜지는데, 이미 점유당한 80 PORT를 사용하지 못해 오류 발생
- `pkill`을 통해 80 PORT를 사용하는 모든 프로세스를 종료하고, `nginx start` -> 해결!