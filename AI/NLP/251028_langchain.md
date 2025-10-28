# Langchain

- https://docs.langchain.com/oss/python/langchain/quickstart

- 1.0.2 버전으로 학습



## 질문 / 답변

- Q1. 아무 도구 안 쓰면 단일 LLM이 작동하잖아. 이거 비활성화하고 도구만 쓰게 할 수는 없나?

  - 되지. 근데 기본 LLM 응답이라는게 모든 도구가 필요 없다고 판단했을 때 사용하는 fallback이기 때문에, 비활성화하려면 명시적으로 조건을 넣어야 하도록 만들어놓은 것.

  - model 호출할 때 `tool_choice="any(or required)"`같은 거 넣어서 모델 단에서 처리할 수도 있고..

  - 그게 안 되는 경우라면 langchain 단에서 차단해야 하는데, tool_call에다 미호출에 대한 예외처리를 하거나 langgraph 레벨에서 차단하거나.. 여러 방법이 있긴 한데, 시스템 안정성 유지를 위해 그냥 프롬프트로 차단하는 방법을 권장하고 있음.

    ```markdown
    You MUST always call a tool to produce an answer.
    If no tool is applicable, respond with: "NO_TOOL_AVAILABLE".
    Never answer directly.
    ```