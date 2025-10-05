# Miniconda 설치 가이드

- 윈도우 OS 환경을 가정한 Miniconda 설치 가이드입니다.

- https://www.anaconda.com/



## 설치

### 1. **Free Download 클릭**

![](./miniconda1.png)

### 2. **Skip registration 클릭**

![](./miniconda2.png)

### 3. OS에 맞는 Miniconda installer 다운로드

![](./miniconda3.png)

### 4. 설치파일 실행 후 기본 옵션으로 설치 진행

![](./miniconda4.png)



## 환경 변수 등록

### 1. **시스템 환경 변수 편집 검색 및 실행**

![](./miniconda5.png)

### 2. 고급 탭 - 환경 변수 클릭

![](./miniconda6.png)



### 3. 사용자 변수 or 시스템 변수 Path를 선택한 후 편집 클릭(둘 중 하나만 하세요!)

![](./miniconda7.png)

### 4. 새로만들기 클릭 후 두 개의 경로 추가

- anaconda3과 그 하위에 있는 Scripts 디렉토리 등록
- 사용자 이름 및 conda 설치 경로에 따라 경로가 달라지니 주의하여 등록

![](./miniconda8.png)



## Conda-forge 채널 등록

- conda 설치 확인

  `conda --version`

- conda-forge 채널 등록

  `conda config --add channels conda-forge`

  `conda config --set channel_priority strict`

- 설정 확인

  `conda config --show channels`

  `conda config --show channel_priority`