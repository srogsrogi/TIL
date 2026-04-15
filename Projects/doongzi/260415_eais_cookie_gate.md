# 세움터 건축물대장 자동 발급 모듈 트러블슈팅

- 둥지 프로젝트 건축물대장 스크래핑 모듈 트러블슈팅



## 상황 요약

- 좀 전까지 되던 건축물대장 발급 워커가 Step 10(발급 신청) 시점에 갑자기 실패하기 시작
  - 세움터 사이트에서 띄운 JavaScript alert에 의해 `UnexpectedAlertPresentException` 발생

```
selenium.common.exceptions.UnexpectedAlertPresentException:
Alert Text: 인증서 프로그램 초기화 시간 만료로 최신 버전 다운로드를 시도해주십시오.
Message: unexpected alert open
  (Session info: chrome=147.0.7727.56)
```

- 프론트 JS 번들 해시는 성공/실패 run 모두 동일 (클라이언트 변경 없음)
- 내가 직접 크롬으로 세움터에 접속하면 발급 정상 동작



## 1차 가설: Headless 탐지

### 문제 & 원인

- Chrome `--headless=new` 모드를 세움터가 탐지해서 cert 분기 태운 것으로 의심
- `navigator.webdriver`, user-agent, AutomationControlled 플래그 등이 노출되고 있음



### 조치 사항

- headless stealth 옵션 추가

  - `--disable-blink-features=AutomationControlled`, `excludeSwitches=[enable-automation]`, custom user-agent, CDP `Page.addScriptToEvaluateOnNewDocument` 로 `navigator.webdriver` 오버라이드 등

- 결과: Chrome CDP 자체가 hang, step 1에서 `ReadTimeoutError` 발생. stealth 옵션이 오히려 드라이버를 망가뜨림

  ```
  ReadTimeoutError("HTTPConnectionPool(host='localhost', port=61715):
  Read timed out. (read timeout=120)")
  ```

- stealth 패치 전부 원복



## 2차 가설: Chrome 147 자동 업데이트

### 문제 & 원인

- `C:\Program Files\Google\Chrome\Application\147.0.7727.56` 디렉토리가 오늘 오전 생성됐음을 발견
- 됐던 run은 146, 지금 안 되는 run은 147 → Chrome이 사이에 자동 업데이트된 것 아닐까



### 조치 사항

- Chrome for Testing 146.0.7680.165를 `C:\chrome-for-testing`에 설치

- `.env.local`에 `CHROME_BIN`/`CHROMEDRIVER_PATH`로 146 경로 명시

- 로그로 `chrome=146.0.7680.165` 확인까지 했으나 **동일한 Step 10 실패 재현**

- Chrome 버전 요인 배제, 변경 전부 원복



## 3차 가설: INISAFE 인증서 모듈 필요

### 문제 & 원인

- Step 3에서 "인증서 관리 모듈이 설치되지 않았습니다" alert 발견
- Step 10의 "인증서 프로그램 초기화 시간 만료"와 같은 계열 메시지
- 세움터가 GPKI 계열 네이티브 플러그인을 요구하는 것으로 추정



### 조치 사항

- `tasklist`로 cert 플러그인 프로세스(`inisafe`, `crosscert`, `wizvera`, `touchen`, `anysign` 등) 검색 → **0건**
- 사용자 직접 크롬에선 플러그인 없이도 발급 정상 동작 → 플러그인이 진짜 게이트면 수동 플로우도 깨져야 정상

- 플러그인 이론 기각



## 4차 가설 → 쿠키 게이트

### 가설 뒤집기

헤드풀 모드(`headless=False`)로 한 번 돌렸더니 즉시 성공. 이후 헤드리스로 되돌려도 성공 지속.

당시엔 "사용자가 수동 허용한 Chrome 네이티브 프롬프트가 프로필에 저장된 것"으로 추정했으나, `Default/Preferences` JSON을 뒤져본 결과 세움터 관련 키/프로토콜 핸들러 기록 없음. 이 가설도 틀림.



### 쿠키 바이섹트

- 진짜 차이를 찾기 위해 `driver.get_cookies()` 덤프해서 incognito run과 프로필 재사용 run 비교

```python
self.logger.info(
    "[COOKIE_DUMP after_step1] %s",
    [(c["name"], c.get("domain"), len(str(c.get("value", ""))))
     for c in self.driver.get_cookies()],
)
```

- 결과

| 쿠키 | incognito (값 길이) | 프로필 재사용 (값 길이) |
| --- | --- | --- |
| SESSION | 48 | 111 |
| clientid | 12 | 75 |
| TMOSHCooKie | 108 | 171 |
| SCOUTER | 14 | 77 |
| WMONID | 11 | 74 |
| **EAISP** | **없음** | **894** |
| JSESSIONID | 없음 | 113 |

- incognito는 매 run마다 **초기 스텁 값**만 받고 `EAISP`(894 bytes)는 아예 부재
- 프로필 재사용은 이전 세션에서 받은 **확장된 실제 상태값**을 누적 보유
- 세움터 서버는 incognito의 쿠키 상태를 보고 cert 체크 분기를 발동시켜 alert를 띄우는 구조



### incognito 모드 특성

- `--incognito`는 베이스 프로필 위에 뜨는 임시 격리 창
- **읽기**: 확장프로그램, 북마크, 설정, 저장 비밀번호 (베이스 프로필)
- **격리**: 쿠키, localStorage, IndexedDB, cache, 히스토리 (세션 종료 시 증발)
- 베이스 프로필에 `EAISP`가 있어도 incognito는 못 봄 → 쿠키 기반 게이트를 우회할 수 없음



### 왜 예전엔 됐을까?

incognito는 처음부터 EAISP를 못 갖는 구조인데 2개월간 멀쩡히 됐음. 즉 **세움터가 2026-04-14 오후 어느 시점에 서버사이드 플래그를 켜서 "EAISP(혹은 확장 쿠키) 없으면 cert 분기"를 활성화**한 것으로 거의 확정. 클라이언트 쪽에서는 확인 불가.



### 조치 사항

- `building_ledger_issuance.py`에서 `--incognito` 제거, `--user-data-dir=<프로필 경로>` 지정

  ```python
  profile_dir = os.getenv(
      "CHROME_PROFILE_DIR",
      os.path.abspath(
          os.path.join(os.path.dirname(__file__), "..", "..", ".chrome-profile")
      ),
  )
  os.makedirs(profile_dir, exist_ok=True)
  options.add_argument(f"--user-data-dir={profile_dir}")
  ```

- `.env.local` / `.env.example`에 `CHROME_PROFILE_DIR` 환경변수 정의

- 최초 1회 `headless=False`로 돌려 프로필에 쿠키를 적재한 뒤, 이후 헤드리스 run에서 동일 프로필 재사용

- 클린 백업을 `references/chrome-bot-profile.bak`에 보관, 복구 절차를 README에 문서화



## 소감

- 아무 것도 안 건드렸는데 갑자기 안 되는 어이가 없는 버그. 서버 측 로그를 볼 수 없으니 해결 과정도 그 동안 해본 것들과는 좀 달랐다. 이것저것 추측해볼 수밖에 없는 구조.
- 외부서비스 의존성의 무서움을 느낌. 등본쪽이나 건축물대장쪽이나 원래 이렇게 쓰라고 만들어놓은 페이지도 아니니까 오류도 잦고 디버깅도 어렵다.
- 이런 식이면 웹훅 알림 걸어 놓고 오류 발생할 때마다 내가 직접 대응할 수밖에 없는데..
  - 아니면 fallback으로 headless=false로 돌려보게 한다거나
  - 서버 측 업데이트에 대응할 수 있는 몇 가지 방법을 스킬로 만들어두고 openclaw나 claude cowork류의 에이전트가 임시로 선대응할 수 있게 짜볼 수도 있을 것 같은데
  - 재밌긴 하겠지만 100%에 가까운 가용성 확보는 어차피 불가능할 것 같고 급한 작업이 많아서 일단 미룸