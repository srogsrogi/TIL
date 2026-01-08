# GKE 실습



## 배경

- Life-Learn 프로젝트
  - 2주 정도 2인 개발한 프로젝트. 시간이 빠듯해서 못 챙긴 부분들이 좀 있음
  - docker-compose로 containerization하고 self-hosting했는데..
  - 서버 배포할 겸 GKE 써볼 겸 마이그레이션



## 설치

- Google Cloud CLI 설치
  - https://docs.cloud.google.com/sdk/docs/install-sdk?hl=ko
- `compose.yml` 파일 k8s용 yml파일로 마이그레이션
  - kompose 설치하긴 했는데.. 이제 그냥 코딩 어시스턴트에게 맡겨서 작성하는게 더 나은 듯
  - self-hosting한 기기 사양이랑 서버 사양도 다르고, k8s에서 추가해줘야 하는 설정 등도 틀을 잡아줌



## 설정

- gcloud CLI로그인
  - `gcloud auth login`
- 프로젝트 지정
  - `gcloud config set project [project_id]`
    - google cloud console에서 project id 확인 가능
- GKE, 이미지 저장소 사용 설정
  - `gcloud services enable container.googleapis.com artifactregistry.googleapis.com`
- 나의 이미지 저장소 생성
  - `gcloud artifacts repositories create my-repo --repository-format=docker --location=asia-northeast3 --description="Docker Repository"`

- Docker 인증
  - `gcloud auth configure-docker`

- GKE 인증 플러그인 설치
  - `gcloud components install gke-gcloud-auth-plugin`
- Cluster 생성
  - `gcloud container clusters create lifelearn-cluster --zone asia-northeast3-a --num-nodes 1 --machine-type e2-standard-2`



## smoke test

- nginx 띄워 보기
  - `kubectl run test-nginx --image=nginx`

- pod 잘 떴는지 확인

  - `kubectl get pods`

- 삭제

  - `kubectl delete pod test-nginx`

  

## 배포

- 빌드 -> 배포 -> 실행 자동화 스크립트 작성(`scripts/deploy.sh`)

  ```sh
  # 에러 발생 시 스크립트 중단
  set -e
  
  # 사용법 안내
  if [ -z "$1" ]; then
      echo "사용법: ./scripts/deploy.sh <GOOGLE_CLOUD_PROJECT_ID>"
      echo "예시: ./scripts/deploy.sh my-awesome-project"
      exit 1
  fi
  
  PROJECT_ID=$1
  
  echo "========================================================"
  echo "🚀 배포 시작: 프로젝트 [$PROJECT_ID]"
  echo "========================================================"
  
  # 1. Backend 빌드 및 푸시
  echo "--------------------------------------------------------"
  echo "📦 Backend 이미지 빌드 중..."
  docker build -t gcr.io/$PROJECT_ID/moduway-backend:latest ./backend
  
  echo "⬆️  Backend 이미지 푸시 중..."
  docker push gcr.io/$PROJECT_ID/moduway-backend:latest
  
  # 2. Frontend 빌드 및 푸시
  echo "--------------------------------------------------------"
  echo "📦 Frontend 이미지 빌드 중..."
  docker build -t gcr.io/$PROJECT_ID/moduway-frontend:latest ./frontend/project-moduway
  
  echo "⬆️  Frontend 이미지 푸시 중..."
  docker push gcr.io/$PROJECT_ID/moduway-frontend:latest
  
  # 3. K8s YAML 파일 이미지 주소 업데이트 (sed 사용)
  echo "--------------------------------------------------------"
  echo "📝 Kubernetes 설정 파일 이미지 주소 업데이트..."
  
  # 운영체제 확인 (Mac용 sed와 리눅스/윈도우용 sed 호환성 처리)
  if [[ "$OSTYPE" == "darwin"* ]]; then
      SED_CMD="sed -i ''"
  else
      SED_CMD="sed -i"
  fi
  
  # Backend YAML 수정
  # 기존 이미지 주소 패턴을 찾아 교체
  $SED_CMD "s|image: .*moduway-backend.*|image: gcr.io/$PROJECT_ID/moduway-backend:latest|g" k8s/05-backend.yaml
  
  # Frontend YAML 수정
  $SED_CMD "s|image: .*moduway-frontend.*|image: gcr.io/$PROJECT_ID/moduway-frontend:latest|g" k8s/06-frontend.yaml
  
  echo "✅ YAML 파일 업데이트 완료"
  
  # 4. GKE 배포
  echo "--------------------------------------------------------"
  echo "🚀 Kubernetes 클러스터에 배포 적용 중..."
  kubectl apply -f k8s/
  
  echo "========================================================"
  echo "🎉 배포가 완료되었습니다!"
  echo "상태 확인: kubectl get pods -n moduway"
  echo "서비스 확인: kubectl get svc -n moduway"
  echo "========================================================"
  ```

- 스크립트 사용 권한 설정
  - `chmod +x scripts/deploy.sh`
- 스크립트 실행
  - `./scripts/deploy.sh [project_id]`



## Cloudflare 설정 변경

- 프론트엔드 pod의 external-IP 확인
  - `kubectl get svc -n lifelearn lifelearn-frontend`
- cloudflare 접속해서 external-IP 입력

- `https://www.life-learn.site` 접속 성공!



## DB 및 ES 설정

- 로컬에 있는 json이나 csv 데이터들과 감성분석모델은 미포함하여 빌드했으니
- 서버로 전송해서 구성 완료한 후 원본 데이터들은 삭제해서 경량화할 예정
- 만들어둔 설정 모듈들에 path 옵션을 넣어 바뀐 경로에도 대응할 수 있도록 해놓음



## 질문/답변

- Q1. 근데 여기선 dockerhub 못쓰고 꼭 나만의 이미지저장소 만들어야 하는 거야?
  - Dockerhub 사용도 물론 가능
  - 근데 public으로 올려도 되는 이미지가 아니라면 K8s에도 Dockerhub 인증정보를 등록하는 별도의 과정이 필요
  - Google Artifact Registry는 디폴트가 비공개고, 구글 거라서 속도도 더 빠름
- Q2. 보안은 구글클라우드가 알아서 하는 거야?
  - ㄴㄴ 어차피 .env같은 건 이미지 만들 때 dockerignore로 빼잖아
  - K8s 만든 다음 `kubectl create secret` 명령어로 클러스터에 직접 넣을 것

- Q3. 이제 self-hosting할 거 아니니까 cloudflare 통하지 않고 namecheap DNS 설정에 직접 주소 넣어도 되는 거 아닌가?
  - 그래도 되긴 하지. 근데 cloudflare가 SSL도 편하게 달아 주고 보안도 조금 챙겨주니까.. 이번엔 굳이 빼고 직접 서버에 SSL 인증서 발급받아줘야 할 이유는 없음