# 가상 환경과 Conda



## 선수 지식

- Python 기초 구문 및 pip 사용법



## 학습 목표

- 가상 환경의 필요성을 설명할 수 있다.
- venv와 conda의 차이를 설명할 수 있다.
- Conda 가상환경을 생성 및 관리할 수 있다.
- 가상 환경에서 패키지 종속성을 저장하거나 불러올 수 있다.



## Warm-up

- 강의계획서 일부 수정되었습니다. 우리의 커리큘럼은 다음과 같습니다.
  - **환경 격리**를 통해 내가 개발한 애플리케이션 포장하기
  - **클라우드 서버**에 내 앱 배포하기
  - **DNS와 SSL**로 도메인 세팅하기
  - 앱 **배포 자동화**하기(CI / CD)
  - 웹 앱에 **DB 연동**하기
  - 마무리 세션
- 오늘 수업에서 다룰 가상 환경과 Docker container는 모두 **환경 격리**를 위한 기술입니다.

- 개발부터 배포로 이어지는 전체 과정에서, 차시마다 배우는 개념 또는 기술이 어떤 역할을 하는지 생각하며 배워봅시다.



## 이론

### 가상 환경의 필요성

- 의존성 충돌 방지
  - 각 앱이 같은 라이브러리의 다른 버전을 요구해서 발생하는 충돌을 사전에 방지
  - 앱 실행에 필요한 최소한의 구성만을 담아 최적화 가능
- 재현성 보장
  - 다른 공간에서도 앱이 동일하게 실행될 수 있도록 함
  - 전혀 다른 OS를 사용하는 경우에는 재현성이 보장되지 **않을** 수 있음



### Conda

- **범용** 환경 / 패키지 관리 도구
  - Python 뿐만 아니라 C/C++, R, Node.js 등 다른 언어 기반 라이브러리도 관리 가능
  - 언어별 버전까지 자유롭게 지정하여 가상 환경 생성 및 관리
  - pip처럼 패키지 관리 기능 수행, OS 레벨 의존성까지 함께 관리

- 두 종류의 배포판 제공
  - Miniconda : conda와 Python만 들어 있는 최소한의 구성
  - Anaconda : 데이터 분석용 대표 패키지가 미리 설치되어 있음
  - Miniconda를 사용하고, 필요한 패키지는 직접 설치해서 쓰는 것이 일반적



### Venv | Conda 비교

| 구분                   | **venv**                                               | **conda**                                                 |
| ---------------------- | ------------------------------------------------------ | --------------------------------------------------------- |
| **개념**               | Python 표준 라이브러리에 포함된 **가상환경 관리 도구** | Anaconda/Miniconda에 포함된 **환경 + 패키지 관리 시스템** |
| **재현성**             | OS가 다를 경우 재현성 낮음                             | OS가 달라도 비교적 재현성 높음                            |
| **의존성 해결**        | 사용자가 직접 관리                                     | 의존성 충돌 자동 해결                                     |
| **시스템 의존성 관리** | 불가능                                                 | 가능 (libssl, gcc 등 함께 관리)                           |
| **속도 및 용량**       | 가볍고 빠름                                            | 느리고 무겁지만 안정성 높음                               |
| **주 사용처**          | 단순한 Python 프로젝트                                 | 데이터 분석, ML, 복잡한 프로젝트                          |



## 실습

### Miniconda 설치 및 초기 설정

- https://github.com/srogsrogi/TIL/blob/master/Lesson/how_to_install/miniconda.md



### conda CLI

- 가상 환경 생성

  `conda create -n <env_name> python=3.12`

- 활성화

​	`conda activate <env_name>`

- 비활성화

  `conda deactivate`

- 삭제

  `conda remove -n <env_name> --all`

- 가상 환경 목록 확인

  `conda env list`



### conda 패키지 관리

- 패키지 설치

  `conda install numpy==1.26.4`

  `pip install requests`

- 패키지 삭제

  `conda remove requests`

- 현재 환경의 패키지 목록

  `conda list`



### conda 환경 관리

- 환경 내보내기 : conda 환경의 복제

  - 설치되어 있는 모든 패키지 기록

    `conda env export > environment.yml`

  - conda로 직접 설치한 패키지만 기록

    `conda env export --from-history > environment.yml`

- 내보낸 파일로 새 환경 생성

  `conda env create -f environment.yml`

- 패키지만 내보내기 : Python 패키지 호환성만 기록

  `conda list export > requirements.txt`



## Wrap-up Quiz

- 가상 환경을 사용하는 이유는 무엇인가요?
- venv와 conda의 차이점은 무엇이 있을까요?
- --from-history 옵션의 장점과 한계점에 대해 말해봅시다.



## 강의 마무리

- 프로젝트든 개인 실습이든 항상 주제별로 가상 환경부터 생성하고, 의존성을 파일 기반으로 관리하는 습관을 가집시다.
- 초보일수록 시스템 레벨에서 패키지를 관리해주는 conda가 더 powerful하니 적극 활용합시다.

- `conda install`과 `pip install`을 섞어 쓸 경우 패키지 관리가 힘들어질 수 있습니다.
- conda 가상 환경에서는 `conda install`을 우선적으로 사용하고 pip는 conda에 없는 패키지를 설치할 때만 보조적으로 활용합시다.



##### ※ venv와 docker 수업이 하루에 진행되어 학생 피드백 및 감상은 docker 문서에 기록함