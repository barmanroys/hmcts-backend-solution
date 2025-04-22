#### Goal

I came across the [developer challenge](https://github.com/hmcts/dts-developer-challenge) which is, apparently, part of
the hiring process for HMCTS[^1]. I am not a frontend/UI guy, so decided to give a shot at the backend and database
components.

#### Application

Basically a MySQL server containing a `tasks` table with which you can interact using a FastAPI backend application.

#### Start Up

Make sure you have docker compose set-up and the following environment variables are available in your POSIX
environment.

| Environment <br/> Variable | Value                                                   
|----------------------------|---------------------------------------------------------|
| MYSQL_DATABASE             | `db`                                                    | 
| USER                       | Usual POSIX user name, will be used for database access | 
| MYSQL_PASSWORD             | Any value you want                                      | 

Given this condition, at the project root, you have to run

```Shell
docker compose up
```

The OpenAPI documentation should be available [on your browser](http://127.0.0.1:8080/docs) to interact.

#### ToDo

* Testing and CI pipeline
* Migration to Kubernetes and ArgoCD

[^1]: I have not verified the affiliation of their GitHub homepage to the real HMCTS, so beware there.