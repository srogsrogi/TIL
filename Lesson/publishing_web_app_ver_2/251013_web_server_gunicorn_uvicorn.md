# WSGI | ASGI



## 선수 지식

- Python 기초 구문 및 pip 사용법
- CLI에 대한 이해
- 웹 프레임워크를 통한 개발 경험 또는 웹 관련 기초 개념



## 학습 목표

- 웹 개발에서 동기와 비동기 방식의 차이에 대해 설명할 수 있다.
- 선택한 웹 프레임워크에 따라 적절한 서버 실행용 라이브러리들을 설치할 수 있다.
- Dockerfile에 Gunicorn 또는 Uvicorn을 통해 개발한 웹앱을 실행하는 구문을 작성할 수 있다.



## Warm-up

- DJango 수업을 들으시면서, `python manage.py runserver`로 로컬 서버를 실행해보셨을텐데요.
- runserver는 개발용 임시 서버이고, 실제 서버 환경에서 웹 앱이 실행되기 위해서는 요청과 응답을 처리하는 서버 앱이 따로 필요합니다.
- 데이터의 입·출력을 담당하는 서버의 역할에 대해 알아봅시다.



## 이론

### 동기 | 비동기

- 동기(Synchronous)

  - 요청을 보낸 후 응답이 올 때까지 대기

  - 작업을 순차적으로 처리

    ```python
    response = requests.get("https://api.com/data") # <- response가 늦게 오면
    print(response.text) # <- 이 구문은 response가 올 때까지 실행되지 않고 기다림
    ```

- 비동기(Asynchronous)

  - 요청을 보낸 후 응답을 기다리지 않고 다른 작업을 수행

  - 동시에 여러 요청을 처리

    ```python
    async def async_example(request):
        async with aiohttp.ClientSession() as session:
            # 외부 API 호출 (비동기)
            get_api_data = session.get("https://api.com/data")  
            # 동시에 다른 작업 수행
            print("다른 작업 하는 중...")
            await asyncio.sleep(1)
            
            # 이제 API 응답 받기
            async with await get_api_data as response:
                data = await response.json()
    
        return JsonResponse({
            "message": "비동기 요청 완료!",
            "api": data["user"]
        })
    ```



### 동기 | 비동기 활용

- 동기 방식은 구조가 단순하고 디버깅하기 쉬우며 안정적으로 작동함
- 비동기 방식은 동시 처리를 통해 전체적인 성능을 올려 주지만, 복잡한 구조로 인해 버그가 발생하기 쉬움
- 상황에 따라 두 방식을 적절하게 선택하고 복합적으로 활용해야 함



### WSGI | ASGI

- WSGI와 ASGI는 서버가 요청을 전달하고 응답을 받는 방식에 대한 규약
- WSGI는 동기 방식으로 처리 | ASGI는 비동기 방식으로 처리

- Python의 대표적인 웹 프레임워크 **Django|FastAPI** 비교
  - **Django**는 WSGI(동기)를 기반으로 하고 비동기 처리 방식도 사용 가능. 전통적인 **웹 개발**에 활용
  - **FastAPI**는 ASGI(비동기)를 좀 더 적극적으로 지원하는 프레임워크. **API 서버** 개발에 활용



### Gunicorn | Uvicorn

- Python 웹 앱을 실행시키는 서버 애플리케이션
- 직접 요청을 받는 것도 가능하지만, 일반적으로 보안 및 성능을 위해 Nginx 뒤에서 동작
- **Gunicorn**은 WSGI 서버. Django|Flask에 최적화
- **Uvicorn**은 ASGI 서버. FastAPI|Django의 ASGI 기반 코드에 최적화



## 실습

- Django 프로젝트의 `wsgi.py`, `asgi.py` 확인
- wisheasy 프로젝트 구조 확인 및 코드 읽어 보기
  - `requirements.txt` : gunicorn
  - `Dockerfile` : 마지막줄 서버 실행 구문



## Wrap-up Quiz

- 동기-WSGI | 비동기-ASGI의 개념을 비교하여 설명해보세요.
- 웹 개발에서 동기 방식과 비동기 방식이 함께 활용되어야 하는 이유는 무엇인가요?



## 강의 마무리

- 서버에 대해 자세히 알지 못하더라도 DevOps의 큰 흐름을 이해하는 데는 큰 지장이 없습니다.
  - Django 앱과 같은 컨테이너 안에서 실행되고, 서버 앱을 호출하거나 건드릴 일이 잘 없습니다.
  - 따라서 이번 차시에서는 명령어를 통해 직접 서버를 실행해보는 실습은 생략합니다.
- 그래도 가볍게라도 개념을 짚고 넘어가는 이유는..
  - 이후의 학습 내용인 Nginx, CI-CD에서 반복적으로 서버 앱을 다루게 되고
  - 웹 개발을 하는 데 있어 동기|비동기를 구분하여 로직을 설계하는 것이 매우 중요하기 때문입니다.
- 핵심 개념들의 관계성을 중심으로 가볍게 복습해주세요!