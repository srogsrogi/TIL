# k8s 실습2

- 첫 실습때 wsl 위에서 minikube 등 설치하고 cluster 및 pod 실행해봤고
- 다른 기능들 차례로 실습해볼 것



## 주요 기초 명령어

- `kubectl get pods`

- `kubectl describe pod <selector>`
- `kubectl delete -f pod.yaml`



## 서비스 만들기

- 인터넷에 pod 노출

  - `kubectl expose deployment <selector> --type=LoadBalancer --port=8080`

  - `--type=LoadBalancer`옵션은 클러스터 외부 서비스로의 노출을 의미함



##### 중간 기록

이것저것 해보면서 CLI 익숙해지고 있는데 아직 정리하기엔 좀 부족해서 일단 덮어둠

SSAFY 공용PC라 방화벽이 외부접근 막고 있어서 local주소는 작동하고 외부로 expose한 주소는 작동을 안 해서

kubectl port-forward로 강제맵핑하니까 됨. 자세한 건 좀더 공부해보고 기록할 것