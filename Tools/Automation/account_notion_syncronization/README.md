# Kakao Bank Transaction Sync to Notion

카카오뱅크 거래내역서(PDF)를 노션 데이터베이스에 자동으로 동기화하는 Python 스크립트입니다.



## 주요 기능

- **PDF 파싱**: `pdfplumber`를 사용하여 카카오뱅크 거래내역서 PDF에서 텍스트를 추출합니다.
- **데이터 정제**: 날짜, 시간, 입/출금 구분, 금액, 잔액, 메모 등을 자동으로 분리하고 정제합니다.
- **중복 방지**: 이미 노션에 등록된 거래내역은 건너뛰고 새로운 내역만 저장합니다. (날짜(분 단위), 금액, 입/출금 구분을 기준으로 중복 확인)
- **자동 업로드**: 노션 API를 통해 추출된 데이터를 지정된 데이터베이스에 자동으로 추가합니다.



## 사전 준비


### 1. 필수 라이브러리 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 아래 정보를 입력하세요.

```ini
NOTION_TOKEN=your_notion_integration_token
DATABASE_ID=your_database_id
PDF_PATH=path/to/your/transaction_history.pdf
```

- **NOTION_TOKEN**: [Notion Developers](https://www.notion.so/my-integrations)에서 생성한 토큰 (Internal Integration Token)
- **DATABASE_ID**: 연동할 노션 데이터베이스의 ID (데이터베이스 URL에서 `https://www.notion.so/{workspace_name}/{database_id}?v=...` 부분 확인)
- **PDF_PATH**: 동기화할 카카오뱅크 거래내역서 PDF 파일의 경로

### 3. Notion 데이터베이스 설정

스크립트가 올바르게 작동하려면 노션 데이터베이스에 **정확히** 아래와 같은 속성(Property)들이 존재해야 합니다.

| 속성 이름 | 속성 유형 (Type) | 설명 |
| --- | --- | --- |
| **구분** | 제목 (Title) | 입금, 출금 등 (페이지 제목 역할) |
| **거래일시** | 날짜 (Date) | 거래가 발생한 날짜와 시간 |
| **거래금액** | 숫자 (Number) | 입금 또는 출금액 |
| **거래 후 잔액** | 숫자 (Number) | 거래 후 남은 잔액 |
| **거래내용(메모)** | 텍스트 (Text) | 거래처 또는 메모 내용 |
| **거래구분** | 텍스트 (Text) | 메모에서 추출한 상세 구분 (선택 사항) |

> ⚠️ **주의**: 속성 이름이 다르면 스크립트가 작동하지 않으므로 이름을 정확하게 맞춰주세요.



## 사용 방법

설정이 완료되면 아래 명령어로 스크립트를 실행합니다.

```bash
python syncronize.py
```

스크립트가 실행되면:
1. 지정된 PDF 파일을 읽어 데이터를 추출합니다.
2. 노션 데이터베이스의 기존 데이터를 조회합니다.
3. 중복되지 않은 새로운 거래내역만 노션에 업로드합니다.
4. 결과(저장된 건수, 중복 건너뜀 등)를 터미널에 출력합니다.



## 참고 사항

- **중복 처리 로직**: 노션 데이터베이스에 저장된 `거래일시(분 단위)`, `거래금액`, `구분`이 PDF의 데이터와 일치하면 중복으로 간주하고 저장을 건너뜁니다.
