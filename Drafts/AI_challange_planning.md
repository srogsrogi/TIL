# SSAFY AI Challenge 팀 프로젝트 계획



## Object Detection 개념

- 기초 개념 강의
  - 객체 영역(bounding box) 예측 + 각 객체의 class 예측(분류)
  - one-stage detector | two-stage detector
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

  

## 데이터 정제

- Train-Validation Split
  - Test 데이터셋은 미리 분리하여 제공됨
- Normalization
- Augmentation
  - 다른 하이퍼파라미터들은 도구 써서 tuning하면 되는데..
  - 이건 사람이 직접 tuning해야 해서 주요 작업 중 하나가 될 듯?
- Feature Engineering



## 모델링

- fine-tuning -> 모델 평가 코드 기본 구조 설계
- 튜닝할 하이퍼파라미터 정의
- 하이퍼파라미터 튜닝 도구 설정(Optuna?)



## 학습 실행 및 평가

- yolo 기본 모델 성능 측정(기준선 설정)
- 모델 성능 개선을 위한 `가설 수립 -> 반영한 새 모델 개발 -> 검증 -> 결과 기록` 과정 반복
  - `best.pt` 파일 저장 및 평가 지표 체계적으로 `google sheets` 등에 기록
  - 일정한 시각화 workflow 활용



## 최종 모델 선택

- 가장 성능이 좋았던 모델 선택
  - 사용한 기법 분석
  - 필요시 추가 시각화 자료 생성
  - 보고서 작성



##### 아무렇게나 바꿔서 돌려 보고, 안 되면 그냥 버리고만 반복하지 말고, 체계적으로 계획해서 튜닝하고, 실행해서 검증하고, 평가하는 사이클을 만들자!