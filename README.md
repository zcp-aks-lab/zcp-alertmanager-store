# ZCP Alertmanager Store Repo

zcp-alertmanager-store 는 zcp-alertmanager 이력관리를 위한 데이터 저장소 이다.
zcp-alertmanager 에 데이터를 제공하므로 zcp-alertmanager 보다 먼저 설치되어야 한다.

Docker Image는 Repository가 변경되거나 Tag가 생성되면 자동으로 이미지가 생성된다. 
그 이미지는 아래 주소에서 확인할 수 있다. 

- Docker registry : https://hub.docker.com/r/cloudzcp/zcp-alertmanager-store/

# Installation

zcp-alertmanager-store와 mariadb를 설치해야 하는데 순서는 상관 없다.  


```
$ git clone https://github.com/cnpst/zcp-alertmanager-store.git
# Checkout 1.0.0 
$ git checkout 1.0.0
 
 
# Deploying zcp alertmanager store
$ cd zcp-alertmanager-store/manifests/alertmanager-store
$ kubectl apply -n zcp-system -f ./ --record
 
 
# Deploying mariadb
$ cd ../alertmanager-store-mariadb/
# AKS 인 경우
$ cd ../alertmanager-store-mariadb-aks/
$ kubectl apply -n zcp-system -f ./ --record

```

