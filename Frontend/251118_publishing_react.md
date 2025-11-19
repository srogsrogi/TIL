# react 배포



## Plan

vite구조로 돼있는 react 프로젝트 nginx로 서빙할거야.

도메인 연결하고 ssl인증서도 받아야 하고

구조 잡아놓고 로컬에서 docker로 1개 컨테이너에 멀티스테이지 빌드한 후에 ec2서버에서는 checkout만 해서 쓸 거야

n8n 백엔드 붙일거라 api설계도 필요해

n8n은 별도 서버 안 만들고 SaaS 웹서비스상에서 GUI로 붙일 거야



## Try



### 로컬실행

로컬에서 돌려보기

npm run build

npm install -g serve

serve -s dist -p 8080

#### 결과

실행은 정상, png파일들이 안 불러와짐. 애초에 figma에서 제대로 받아오지를 못 한 듯?



### 이미지 파일 수정

figma에서 사용하는 이미지들 전부 png로 다운로드 및 src/assets에 추가
이미지별 alias와 import 경로 모두 수정

- App.tsx의 import문과 아래에서 실제로 사용하는 imageUrl
- 각 tsx파일
- vite.config.ts

#### 결과

얼추 되긴 했는데 png파일이 배경 흰색인 걸로 저장돼서 배경이 흰 색이 아닌 곳에서 이미지가 쓰일 때 흰 박스가 그대로 보임. 배경 없앤 버전으로 만들고 경로만 똑같이 해서 재빌드하면 됨

이미지 매핑 눈대중으로 한거라 제자리에 올바른 이미지 들어갔는지 확인 필요

일단 띄우는게 중요해서 1차배포부터 시도해보고 나중에 하는 걸로



## dockerfile

