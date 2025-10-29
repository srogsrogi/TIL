# Langchain

- https://docs.langchain.com/oss/python/langchain/quickstart

- 1.0.2 버전으로 학습



## Agent 구성 요소

- model

  - 역할

    - agent의 추론기 역할
    - agent loop 외부에서 독립된 작업 수행

  - 종류

    - api
    - local llm

  - invoke | stream | batch

  - 사용법

    - init

    - callback

    - config

      

- message

  - 단일 텍스트 프롬프트 요청
  - message 프롬프트
    - message 객체들을 []로 묶어 model에 전달
      - SystemMessage : 분위기, 역할, 지침 등
      - HumanMessage : 사용자 입력
      - AIMesaage : 메타 데이터를 포함한 LLM의 출력 전체. 도구 호출 정보 포함
  - dict 형식 프롬프트
    - role
    - content

- tool

  - typehint
  - docstring
  - custom tool | model server 제공 tool
  - toolruntime

- streaming

- middleware

- structured response

  - raw json
  - 커스텀 @dataclass
  - pydantic



## 질문 / 답변

- Q1. 아무 도구 안 쓰면 단일 LLM이 작동하잖아. 이거 비활성화하고 도구만 쓰게 할 수는 없나?

  - 되지. 근데 기본 LLM 응답이라는게 모든 도구가 필요 없다고 판단했을 때 사용하는 fallback이기 때문에, 비활성화하려면 명시적으로 조건을 넣어야 하도록 만들어놓은 것.

  - model 호출할 때 `tool_choice="any(or required)"` 넣어서 모델 단에서 처리할 수도 있고..

  - 그게 안 되는 경우라면 langchain 단에서 차단해야 하는데, tool_call에다 미호출에 대한 예외처리를 하거나 langgraph 레벨에서 차단하거나.. 여러 방법이 있긴 한데, 시스템 안정성 유지를 위해 그냥 프롬프트로 차단하는 방법을 권장하고 있음.

    ```markdown
    You MUST always call a tool to produce an answer.
    If no tool is applicable, respond with: "NO_TOOL_AVAILABLE".
    Never answer directly.
    ```



- Q2-1. Docs 보면, ToolRuntime이 tool 사용과 관련된 정보를 통해 tool이 더 똑똑하게 작동하게 해준다는데, tool 자체는 추론 능력이 없는 일반적인 함수/앱일텐데 어떻게 그 text로 된 context를 해석한다는 거야?
  - tool이 직접 그 데이터를 해석하는 건 아니고, 그건 그 tool을 사용하는 agent의 몫이지.
  - 기본적으로 tool과 model은 둘 다 stateless하게 작동하기 때문에, 그 도구를 써온 맥락, 사용자 및 현재 세션에 대한 정보들이 없단 말이야.
  - 그런 context들을 저장하기 위해 ToolRuntime이라는 객체를 tool 호출시 함께 전달하는 거야.
  - ToolRuntime 자체는 그냥 key-value 형식의 텍스트로 된 기록일 뿐인 거지. agent가 추론이나 도구 호출 중에 그걸 활용하는 거고.
- Q2-2. 웹 서비스처럼 상태 관리가 필요한 REST API에서 세션이나 쿠키를 활용하는 거랑 비슷하네. 근데 기본적으로 tool 실행에 필요한 파라미터들이나 typehint, docstring은 tool 구조를 통해서 전달되고, 꼭 ToolRuntime에 따로 기록하지 않더라도 대화 기록 자체는 checkpointer를 통해 메모리에 저장되잖아. 그럼 agent 모델 성능이 좋을 수록 ToolRuntime은 없어도 상관 없는 거 아닌가?
  - ㅇㅇ 실제로 낮은 성능의 모델을 쓸수록 중요성이 더 커짐. context 유지를 위해 보조적인 역할을 수행하는 거지.
  - 그래서 tool에 ToolRuntime을 따로 정의하지 않더라도 tool 사용 자체는 잘만 되고,
  - ToolRuntime을 넣어준 경우라고 하더라도 내부적으로는 kwargs로 작동해서 필수 인자가 아님.
  - 다만 사용자나 세션에 대한 메타 데이터는 이걸로 주입하지 않으면 없는 정보니까, 모델 성능과 관계 없이 tool의 성격에 따라 꼭 필요할 때도 있지. 모델 성능이 좋다고 해서 전혀 필요 없어지는 건 아님.
- Q2-3. 애초에 맥락 유지 자체가 필요 없는 tool들도 있겠다. 가령 계산기 함수 같은 건 그냥 계산만 하면 그만이지 사용자나 사용 기록 같은 거 알 게 뭐야. 어떤 tool들에는 ToolRuntime이 필요하고 어떤 tool들에는 불필요할까?
  - 단순 연산이나 변환, 단발성 API 호출 함수처럼 state가 필요하지 않은 애들은 ToolRuntime을 써줄 필요가 없음
  - 반대로 사용자나 세션별 개인화된 대화가 필요하거나, DB나 vector store를 검색해야 하는 경우나.. context를 필요로 하는 꽤 많은 경우에 ToolRuntime이 필요하지.