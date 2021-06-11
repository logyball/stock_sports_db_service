# Database

There needs to exist a database that is configured in certain ways in order for the stonks project to work.  It needs a historical record of stock prices as well as gambling odds to persist such that data can be compared across time.

# MySQL on K8s

Databases on a container orchestration platform? Whaaa?

[It is possible.](https://kubernetes.io/docs/tasks/run-application/run-single-instance-stateful-application/) The trick is managing credentials.  In order to facilitate this I created several startup scripts.

### Initialization

I needed to create a database, several tables, and at least one non-root user.  If I were really in true DBA nerding out mode, I would create roles and other things.  But for now I'm going to stick to the basics.

#### Database

I created a database named stonks.  It holds all the logic here.

```sql
SET GLOBAL time_zone = '-7:00';
CREATE DATABASE IF NOT EXISTS stonks;
USE stonks;
```

#### Users

I created an admin, a writer, and a reader user.  The writer will have the ability to add info, the reader can read info, and the admin can do whatever.



create secret generic asdf -n stonks --from-file=../../db/startup.sql -o yaml --dry-run=client | kubeseal -o yaml - > tmp.yml