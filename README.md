# Stocks and Gambling

This is the first part of an ongoing project that I'm working on to evaluate the performance of stocks and sports gambling.   [Check out this post](https://loganballard.com/index.php/2021/06/10/stocks-vs-sports-0-inception/) for the background.  This repository implements the data generation and thin layer retrieval service.

![Component Design](./imgs/db-service-design.png "Component Design") 

## Constraints

I am deploying on Kubernetes with the ability to run on ARM architecture.  This means that:
1. Everything must be containerized
2. All containers must _have the option to be_ ARM-based

## Database

The database is created using MySql due to its great documentation, ability to be used easily in Kubernetes, and general flexibility.  It pretty heavy for what I require, and a relational data model may not be the best approach for a completely additive datastore.

#### Deployment

Deploying the database is easy.  Create the required namespace, then create the database objects.

```shell
$ kubectl apply -f ops/Namespace.yml
$ kubectl apply -f ops/db/  # Applies PVC, STS, SVC, Secrets, ConfigMaps
$ kubectl get all -n stocks-sports
NAME          READY   STATUS    RESTARTS   AGE
pod/mysql-0   1/1     Running   0          92s

NAME            TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
service/mysql   ClusterIP   <clust ip>   <none>        3306/TCP   92s

NAME                     READY   AGE
statefulset.apps/mysql   1/1     92s
```

Note that the namespace is required for all objects as this will be where our db and scheduled jobs land.

#### Credentials

In order to get credentials, I used a random password generator and then a [sealed secret](https://github.com/bitnami-labs/sealed-secrets).  This will vary for your cluster.  The command is below:

```shell
$ kubectl create secret generic mysql-credentials --from-literal=root_pass=<secret> --from-literal=admin_pass=<secret> --from-literal=writer_pass=<secret> --from-literal=reader_pass=<secret> -n stocks-sports -o yaml --dry-run=client | kubeseal -o yaml - > ops/db/mysqlCredentials.yml
```

#### Startup Script

Because one of the startup scripts contains secrets, it also had to be obscured.

```shell
$ kubectl create secret generic mysql-startup --from-file=./db/users.sql -n stocks-sports -o yaml --dry-run=client | kubeseal -o yaml - > ops/db/startupSecretScript.yml
```

Of course you'll need to modify the secrets values.

