# ZCP Alertmanager Store Repo
Provide ZCP Alertmanager History Feature

## MariadDB Deploy
helm or Deployment.yaml

## Webhook-Alertmanger-Store Deploy

Docker build
Docker Image Push

# The zcp-alertmanager Installation Guide

zcp-alertmanager-store 는 zcp-alertmanager 이력관리를 위한 데이터 저장소 이다.
zcp-alertmanager 에 데이터를 제공하므로 먼저 설치되어야 한다.

## Clone this project into the desktop
```
https://github.com/cnpst/zcp-alertmanager-store.git
```

## Deploy the application

configuration 파일 디렉토리로 이동한다.

```
$ cd zcp-alertmanager-store/manifests
```

### :one: Mariadb를 설치한다.
```
$ kubectl apply -f alertmanager-store-mariadb
```
### :two: alertmanager-store를 설치한다.
```
$ kubectl apply -f alertmanager-store
```

### :three: 설치확인.
다음 명령어로 zcp-iam 이 정상적으로 배포되었는지 확인한다.
```
$ kubectl get pod -n zcp-system
```

