- - # Nginx, Uvicorn, Gunicorn
  
    
  
    ## 들어가기 전에..
  
    - User, Client, Server 그림(보드에 그림)을 통해 데이터의 흐름 설명
    - proxy라는게 있는데, 물론 없어도 그림처럼 잘 돌아는 가지만..
    - 우리는 그 사이에 proxy 서버를 둬서 뭔가를 중개하도록 만들 것이다!
  
    
  
    ##### 이후 `250811_nginx_uvicorn_gunicorn`으로 수업 진행
  
    
  
    ##### 내일 수업은..
  
    - https와 ssl 인증서에 대한 약간의 설명
    - 실습
      - dockerfile 포트 바꿔서 이미지 재빌드
      - ec2에서 바뀐 이미지로 컨테이너 다시 실행하고 nginx 연결
      - ssl인증서 발급, 리디렉션 설정 및 자동갱신 확인
      - 도메인 접속 확인