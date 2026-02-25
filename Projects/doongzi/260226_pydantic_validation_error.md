# 트러블슈팅: 로컬 및 CI 서버 pytest 실패



## 상황 요약

`make test` 명령어를 사용하여 `pytest` 로 테스트 모듈 실행

→ Pydantic Validation Error 발생

```
# 1차 에러(CI 서버)
E   pydantic_core._pydantic_core.ValidationError: 12 validation errors for Settings
E   SECRET_KEY
E     Field required [type=missing, input_value={}, input_type=dict]
E   POSTGRES_USER
E     Field required [type=missing, input_value={}, input_type=dict]

# 2차 에러(CI 서버)
E   pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings
E   ACCESS_TOKEN_EXPIRE_MINUTES
E     Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='', input_type=str]
```



## 1차 에러

### 문제 &원인

**로컬 환경**

- fastapi 앱의 config에서 settings 객체를 만들 때 `.env.local`을 올바르게 참조하여 settings 객체에 환경 변수가 주입된 경우에는 오류 없이 통과

**CI 서버**

- CI 서버에는 `.env.local` 이 올라가지 않아 환경 변수 누락 Validation Error 발생

### 조치 사항

- `.env.example` 을 ci서버로 `cp` 하여 mock 환경 변수로 CI를 시도하였으나 2차 에러 발생

  ```yaml
        - name: Setup test environment
          env:  
            JUSO_API_KEY: ${{ secrets.JUSO_API_KEY }}
          run: cp .env.example .env.local
  ```



## 2차 에러

### 문제 & 원인

**CI 서버**

- `.env.example` 에 있는 환경 변수는 대부분 빈 문자열로 설정되어 있음
- `pytest` 실행 시 `Pydantic` 모듈이 환경 변수(빈 문자열)를 형변환할 때, type이 `str` 이 아닌 경우 Validation Error를 발생시킴

### 조치 사항

- `int` 형식의 환경 변수에 대하여 `.env.example` 에 기본값 기입

- password hashing에 필요한 설정값 기입

  ```.env.example
  ACCESS_TOKEN_EXPIRE_MINUTES=1440
  ALGORITHM=HS256
  ```



## 3차 에러

### 문제 & 원인

**로컬 환경**

- test 모듈 추가한 후, `pytest` 가 참조하는 환경 변수가 `.env.local`이 아닌  `.env` 로 설정되어 있어 참조 실패 → `make test` 실패

### **해결 방법**

- `pytest` 가 참조하는 환경 변수 파일을 `.env.local` 로 수정
- 모든 이슈 해결 및 CI 테스트 통과



## 요약

CI 환경에서 환경 변수 누락 및 Pydantic 타입 검증으로 인해 발생한 테스트 실패 에러를 더미 환경 변수 파일 생성(`cp .env.example .env.local`)과 유효한 타입 값(정수형 더미 값) 할당으로 해결



## 부록: AI 답변

### 원인

1. **CI 환경의 특성:** 깃허브 레포지토리에는 보안상 실제 환경 변수 파일(`.env.local` 등)이 업로드되지 않습니다. 아무것도 없는 깨끗한 CI 러너(Runner)가 테스트를 돌리기 위해 `config.py`의 `Settings` 객체를 생성하는 순간, 필수 값을 찾지 못해 검증 에러를 뿜어냅니다.
2. **Pydantic의 엄격한 타입 검증:** Pydantic은 값이 비어있는 환경 변수(`KEY=`)를 빈 문자열(`""`)로 인식합니다. 문자열(`str`) 타입은 에러가 나지 않지만, `int`, `float`, `bool` 등의 타입은 빈 문자열을 해당 자료형으로 변환할 수 없어 타입 파싱 에러(`int_parsing`)를 발생시킵니다.

### CI서버 환경 설정 방법

FastAPI와 함께 주로 사용되는 `pydantic-settings` 모듈은 애플리케이션 시작(또는 테스트 스크립트 시작) 시점에 필요한 모든 환경 변수가 정확한 타입으로 존재하는지 검증(Validation)하는 강력한 역할을 합니다.

이러한 특성 때문에 개발자의 로컬 PC에서는 문제없이 돌아가던 코드가 CI 서버(GitHub Actions)에서는 실패하는 현상이 자주 발생합니다. 로컬에는 `.env.local` 파일이 존재하여 값들이 정상적으로 주입되지만, CI 서버는 이를 알 수 없기 때문입니다.

결국 CI 환경에서 로직 테스트(`pytest`)를 무사히 통과시키려면 **진짜 운영 환경과 무관하더라도 Pydantic을 통과할 수 있는 형식에 맞는 가짜(Dummy) 데이터**가 필요합니다. 빈칸(`KEY=`)으로 두면 Pydantic이 이를 빈 문자열로 처리하므로, 정수형(`int`) 변수에는 `1`이나 `1440`을, 논리형(`bool`) 변수에는 `false` 등을 명시적으로 적어두는 것이 CI 에러를 예방하는 올바른 세팅 방법입니다.