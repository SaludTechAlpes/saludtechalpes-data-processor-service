# Description
This is a microservice to handle images 🏞️ processing and anonimization them.

# Made with
[![Python](https://img.shields.io/badge/python-2b5b84?style=for-the-badge&logo=python&logoColor=white&labelColor=000000)]()
[![Flask](https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white&labelColor=000000)]()

# How to execute

If you want execute without docker then you can use the next commands in your terminal.
Note: firstable is important that you have your python virtual environmente created.

into directory flaskr execute
```bash
$ flask run
```

# Prerequirements


* Python 🐍
* Docker & docker-compose 🐳 (Optional).
* For Linux 🐧 and mac 🍎 you can use makefile.
* For Windows 🪟 you can use bash function.

## ⚠️ Important

It is important to have all the projects and repositories in the next folder

# [IMAGE]

# How to execute with docker 🐳

1. Step one locate in the root of the project

```bash
$ cd saludtechalpes-data-processor-service
```

2. Run in docker 🐳

```bash
# With Linux 🐧 or Mac 🍎
$ make docker-local-up

# With Windows 🪟
$ source run.sh; docker_local_up

# With docker compose for all Operative Systems

$ docker compose -f=docker-compose.local.yaml up --build
```

3. Make sure that all microservices are running

* Executing this command

```bash
$ docker ps
```

# [IMAGE]

4. Execute the **health** api rest with cUrl or you could use postman 👩🏻‍🚀 in order to validate the health 💚

```bash
curl --location 'http://localhost:3001/health' --header 'Content-Type: application/json'
```

### Body in JSON

```json
{
    "application_name": "saludtechalpes-data-processor-service",
    "environment": "local",
    "status": "up"
}

```

5. Finally, shutdown the environment in docker 🐳
```bash
# With Linux 🐧 or Mac 🍎
$ make docker-dev-down

# With Windows 🪟
$ source run.sh; docker_local_down

# With docker compose for all Operative Systems

$ docker compose -f=docker-compose.local.yaml down
```
