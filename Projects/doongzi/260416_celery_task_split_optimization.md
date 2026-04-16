# Celery task 분할 구조의 커넥션/배치 비효율

- 독소조항 분석 도메인 PR 리뷰 하다가 발견한 설계 이슈
- 1 요청 = N 조항을 N개의 독립 Celery 태스크로 발행하는 구조의 비효율성 정리



## 구조 요약

- 사용자가 계약서에서 특약 N개를 골라 POST
- backend가 `ClauseTask` row N개를 PENDING으로 생성
- 각 태스크를 `celery_app.send_task("clause.search", args=[clause_text])`로 broker에 N번 발행
- clause-worker가 각 태스크를 독립적으로 pick → RAG 검색(FTS + pgvector) → 결과 반환
- backend가 폴링하며 완료된 태스크에 LLM 호출 + 저장

즉 **1 요청 = N 태스크 = N 워커 처리** 구조. 조항 단위 독립성은 확보되지만 부하 특성이 전부 N배로 곱해짐.



## 문제 1: DB 커넥션 N배 소비

### 현재 동작

clause-worker의 `search` 태스크 내부에서:

- `_fts_search`: `get_connection()` 호출 → 커넥션 1개 열고 닫음
- `_vector_search`: `get_connection()` 호출 → 또 커넥션 1개 열고 닫음

  - `worker/db.py`는 NullPool 패턴(psycopg2 raw connect, 풀 없음)

  - 호출할 때마다 TCP handshake + auth + `SET search_path`까지 매번 수행.

```python
# worker/db.py
def get_connection():
    settings = get_settings()
    conn = psycopg2.connect(
        settings.DATABASE_URL,
        cursor_factory=RealDictCursor,
        options="-c search_path=rag,public",
        connect_timeout=3,
    )
    return conn
```



### 실제 비용

1 요청(10조항)이 들어오면:

- 태스크 10개 × (FTS 1 + vector 1) = **커넥션 생성/종료 20회**
- worker를 수평 확장하면 이 20개가 거의 동시에 RDS로 쏟아짐
- RDS 커넥션 establish는 수십 ms, 반면 HNSW index 조회 본체는 한 자릿수 ms
- 즉 **오버헤드가 본체보다 큼**



### 개선 옵션

| 옵션 | 난이도 | 효과 |
| --- | --- | --- |
| 단일 태스크 내 FTS/vector 커넥션 공유 | 저 | 20→10회. 이번 PR 범위로 가능 |
| `psycopg2.pool.ThreadedConnectionPool` 도입 | 저 | 프로세스당 커넥션 재사용, handshake 제거 |
| PgBouncer 앞단 배치 | 중 | 워커 코드 무변경, 인프라 변경 |
| 요청 단위 배치 태스크로 재구성 | 고 | 근본 해결. 구조 변경 필요 |



## 문제 2: GPU 모델 호출 배치 기회 손실

### 현재 동작

- `embed_query(clause_text)`는 단일 문장 embed
- `rerank(query, passages)`도 태스크별 독립 호출
- 10 조항이면 GPU 호출 최소 20회(embed 10 + rerank 10)



### 배치 가능성

- multilingual-e5-large나 bge-reranker 류 모델은 배치 입력 원래 지원
- 10개 쿼리를 한 번에 embed하면 GPU 웜업/메모리 전송 비용이 1회로 압축됨
- 그런데 현재 API가 단일 문장만 받도록 잡혀 있어서 태스크 단위에서 배치 불가 → **요청 단위 태스크로 묶어야만 가능**



## 문제 3: Celery / broker 오버헤드

- N 태스크 = broker round-trip N회(publish N + result backend write N)
- `result_expires=3600` 동안 N개 결과 key가 Redis에 상주
- 각 태스크마다 backend가 `AsyncResult.ready()` 폴링 → 폴링 비용도 N배



## 왜 이렇게 짰을까

- 조항별 독립성을 구조적으로 보장하고 싶었던 듯
- 외부 API 호출(특히 비용 발생하는 LLM 호출 등)이 필요한 경우 또는 각 task가 서로 다른 로직, 서비스를 호출하는 경우라면 성공한 task만 살리는 게 더 의미가 있음

근데 막상 따져보면..

- 조항별 독립성이 진짜 의미 있는 구간은 **LLM 호출 단계**(backend `_call_llm_and_save`)
- search(RAG 검색) 단계는 조항별 독립일 필요가 없음. 오히려 배치로 묶는 편이 훨씬 효율적
- 즉 **태스크 분할 경계를 search가 아니라 LLM 단계에서 그었어야** 함



## 내가 이번에 바꾼다면

- `clause.search` 태스크를 요청 단위로 묶기: `search(clauses: list[str])` → 내부에서 embed 배치, 하이브리드 검색도 쿼리 묶음으로 처리
- LLM 호출은 기존처럼 조항별 독립 유지(실패 격리 이득이 실제로 있는 구간)
- 이렇게 바꾸면 요청당 커넥션 생성 2회(또는 1회), GPU 호출 2회(embed batch 1 + rerank batch 1)로 떨어짐



## 일반화해서 기억할 것

- Celery 태스크 분할 경계는 **"독립성이 필요한 가장 비싼 지점"** 에 긋는 게 맞음
- 단순히 "병렬 단위"로 잘게 쪼개면 커넥션/GPU/broker 전부에 N배 부하로 꽂힘
- 태스크 분할 구조 리뷰할 때 체크 포인트
  1. 커넥션/네트워크 비용이 N배로 곱해지는가
  2. GPU/모델 로드에 배치 기회를 놓치고 있는가
  3. broker/result backend 오버헤드가 무시 못할 수준인가
  4. 분할 경계가 실제 독립성 요구 지점과 맞는가



## 소감

- 당장은 성능 병목이 있을 만한 상황이 아니라서 가볍게 넘기긴 했는데, worker 스케일 시나리오 떠올리고 나니 훨씬 큰 얘기였음
- 머릿속에서 요청 하나 들어왔을 때 데이터가 어떻게 흘러갈지 tracing이 어느 정도 되니까, 할 수 있는 고민의 깊이가 깊어진다.
