보안그룹 443 열기

sudo apt update

sudo apt install nginx

sudo apt install certbot python3-certbot-nginx



nginx가 80포트를 사용해야 하는데 컨테이너 자체가 80포트를 점유하고 있어서 에러가 나는 상황

컨테이너 중지/삭제한 후 다시 run해야 하는데..

포트 설정은 server.py에 있으니

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]으로 바꿔서 이미지 재빌드하고

그 이미지 받은 후에

docker run -d --name fastapi-app -p 8080:8080 myimage



이후에 

sudo certbot --nginx -d najungh.site --redirect -m junghyun.na321@gmail.com --agree-tos --no-eff-email

이거 해주면 ssl인증서 받아질 것