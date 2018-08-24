# ZCP Alertmanager Store Repo

"Alertmanager Store" is an applicatoin that stores a record of the notification history in the ZCP Alertmanager.

It have only store feature.

# Installation

You can run the following code.

```
$ git clone https://github.com/cnpst/zcp-alertmanager-store.git
# Checkout 0.9.3 
$ git checkout 0.9.3
 
 
# Deploying zcp alertmanager store
$ cd zcp-alertmanager-store/manifests/alertmanager-store
$ kubectl apply -n zcp-system -f ./ --record
 
 
# Deploying mariadb
$ cd ../alertmanager-store-mariadb/
$ kubectl apply -n zcp-system -f ./ --record

```

