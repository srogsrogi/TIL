# SSAFY AI Challenge 팀 프로젝트 계획



## Image Classification | Object Detection 개념 소개

- 이미지 분류 모델

  - 이진 분류 | 다중 분류
  - 주요 모델 : mobilenet, efficientnet, ViT계열 등

- 객체 탐지 모델

  - 객체 영역(bounding box) 예측 + 각 객체의 class 예측(분류)

  - one-stage detector | two-stage detector, segmentation data 사용 여부에 따른 모델 성능

  - 주요 모델 : yolo, R-CNN 계열

  - 평가 지표 : mAP, IoU 개념

    



## 환경 구성

- kaggle notebook(t4)
- optional : local 서버(rtx4070ti)



## 데이터 및 과제 분석

- 이미지 파일 직접 열어 보며 특성 파악

- 라벨링 구조 확인

- 기초 EDA

  - 데이터 분포, class별 데이터 수 확인
  - 이상치 및 결측치 관측 및 처리




## 모델 선택

- 이미지 분류? 객체 탐지?
- 모델별 특징/장단점 학습
- 테스트해볼 모델 목록/우선순위 설정



## 데이터 정제

##### 모델 특성에 맞게 데이터 구조 변환 / 생성 필요

- Train-Validation Split
  - Test 데이터셋은 미리 분리하여 제공됨
- Normalization
- Augmentation
  - 다른 하이퍼파라미터들은 도구 써서 tuning하면 되는데..
  - 이건 사람이 직접 tuning해야 해서 주요 작업 중 하나가 될 듯?
- Feature Engineering



## 모델링

- fine-tuning -> 모델 평가 코드 기본 구조 설계, 랜덤시드 설정
- 튜닝할 하이퍼파라미터 정의
- 하이퍼파라미터 튜닝 도구 설정(Optuna?)
  - 여의치 않으면 손으로 할 수도 있고..


##### ※ 주의

- 모델/버전마다 입력 데이터 형식이 다르고, AI가 그걸 제대로 학습하고 있지 않음
- 공식 문서나 사람이 쓴 코드를 바탕으로 시작할 것



## 학습 실행 및 평가

- 기본 모델 성능 측정(기준선 설정)
- 모델 성능 개선을 위한 `가설 수립 -> 반영한 새 모델 개발 -> 검증 -> 결과 기록` 과정 반복
  - `best.pt` 파일 저장 및 평가 지표 체계적으로 `google sheets` 등에 기록
  - 실행 환경, 학습 및 추론 소요 시간도 기록 필요
  - 일정한 시각화 workflow 활용



## 최종 모델 선택

- 가장 성능이 좋았던 모델 선택
  - 사용한 기법 분석
  - 필요시 추가 시각화 자료 생성
  - 보고서 작성



##### 아무렇게나 바꿔서 돌려 보고, 안 되면 그냥 버리고만 반복하지 말고, 체계적으로 계획해서 튜닝하고, 실행해서 검증하고, 평가하는 사이클을 만들자!

