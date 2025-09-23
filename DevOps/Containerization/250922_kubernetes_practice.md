# Kubernetes 실습

- 기초 개념은 공식문서를 읽으면서 훑고 GPT로 보완함
  - https://kubernetes.io/ko/docs/concepts/overview/

- 개념 범위가 좀 넓어서 다 이해하고서 하긴 어려울 것 같고.. 냅다 실습해보고 그거 기반으로 넓혀나가야겠음



## Docker Desktop 설정

- `Settings` -> `General` -> `Use the WSL 2 based engine` 체크
- `Settings` -> `Resources` -> `WSL integration` -> `Enable integration with my default WSL distro` 체크
- 바로 아래 `Ubuntu` 활성화, `Apply & restart`



## Ubuntu 환경 생성

- Windows CMD
  - Ubuntu 설치
    - `wsl --install -d Ubuntu`
  - username 및 password 지정
  - linux ubuntu 가상환경 실행
    - `wsl -d Ubuntu`
  - Docker 실행 확인
    - `docker version`



## k8s 및 minikube 설치

- kubernetes CLI 설치(root 권한 필요)

  ```bash
  curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
  
  chmod +x kubectl
  
  mv kubectl /usr/local/bin/
  
  kubectl version --client
  ```



- minikube 설치

  ```bash
  curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
  
  sudo install minikube-linux-amd64 /usr/local/bin/minikube
  ```



## Docker 소켓 권한 설정

- docker 그룹에 현재 사용자 추가
  - `sudo usermod -aG docker $USER`
- 현재 셀에 즉시 반영
  - `newgrp docker`
- 소켓 권한 확인
  - ls -l /var/run/docker.sock
  - root:docker 소유, 그룹에 rw 권한이 있어야 정상
- sudo 없이 docker 데몬 붙는지 확인
  - `docker version`



## Cluster 시작

- Docker Desktop을 백엔드로 사용하여 클러스터 시작(일반 사용자로만 가능)
  - `minikube start --driver=docker`

- minikube 동작 확인

  ```bash
  kubectl get nodes
  kubectl create deployment nginx --image=nginx
  kubectl expose deployment nginx --type=NodePort --port=80
  minikube service nginx --url
  ```

- Dashboard 확인

  ```bash
  minikube addons enable dashboard
  minikube dashboard
  ```

  

## Django 앱 생성

- 일단 익숙한 프레임워크로 해봄
- 프로젝트 1개, 앱 1개에 메인페이지 하나만 html로 띄워 놓은 빈 앱 생성



## Dockerfile 작성

- gunicorn으로 django 앱 실행하는 간단한 Dockerfile 작성
- 이건 어차피 kubernetes 안 쓸 때랑 같은 과정이라 설명은 생략



## yaml파일 작성

- deployment.yaml 작성 예시

  ```yaml
  # 1. Service for Django App (for internal communication)
  apiVersion: v1
  kind: Service
  metadata:
    name: django-app-service
  spec:
    selector:
      app: django-app
    ports:
      - protocol: TCP
        port: 8000 # The port the service will listen on
        targetPort: 8000 # The port the container is running on
  
  ---
  # 2. Deployment for Django App
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: django-app-deployment
  spec:
    replicas: 1
    selector:
      matchLabels:
        app: django-app
    template:
      metadata:
        labels:
          app: django-app
      spec:
        containers:
        - name: django-app
          image: srogsrogi/k8s_practice:latest # Your Docker Hub ID is used here
          ports:
          - containerPort: 8000
  
  ---
  # 3. ConfigMap for Nginx Configuration
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: nginx-config
  data:
    nginx.conf: |
      server {
          listen 80;
          server_name localhost;
  
          location / {
              proxy_pass http://django-app-service:8000; # Pass requests to the Django service
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              proxy_set_header X-Forwarded-Proto $scheme;
          }
      }
  
  ---
  # 4. Deployment for Nginx
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: nginx-deployment
  spec:
    replicas: 1
    selector:
      matchLabels:
        app: nginx
    template:
      metadata:
        labels:
          app: nginx
      spec:
        containers:
        - name: nginx
          image: nginx:latest
          ports:
          - containerPort: 80
          volumeMounts:
          - name: nginx-config-volume
            mountPath: /etc/nginx/conf.d
        volumes:
        - name: nginx-config-volume
          configMap:
            name: nginx-config
  
  ---
  # 5. Service for Nginx (to expose it externally)
  apiVersion: v1
  kind: Service
  metadata:
    name: nginx-service
  spec:
    selector:
      app: nginx
    type: NodePort # Using NodePort for easy access in Minikube
    ports:
      - protocol: TCP
        port: 80
        targetPort: 80
  ```

  

## Docker Image Build / Push

- CMD로 열어 놓은 Ubuntu 환경에서 docker 이미지 빌드 및 푸시



## Kubernetes에 앱 배포

- yaml 파일을 통해 배포
  - `kubectl apply -f deployment.yaml`
- 서비스 접속 확인
  - minikube service nginx-service --url



## 결과 및 소감

- 받은 URL 링크로 nginx 통해 웹서버 접속 성공

- 아직은 GPT가 써준 yaml 파일로 텅 비어있는 웹서버 하나 붙인 거고.. 앞으로 세부 설정 보면서 직접 파일 작성해볼 것
- wsl2 위에서 굴려야 하기도 하고, 설치법이나 기본 실행 자체가 docker보단 훨씬 복잡하긴 한데, docker로 여러 번 배포해본 짬바가 있어서 전체적인 구조 이해하고 실습하는 게 딱히 어렵지는 않았음