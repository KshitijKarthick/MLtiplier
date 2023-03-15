# README #

ML Project template used to bootstrap ML projects requiring compute-intensive jobs.

### Features:
* Batching of ML jobs to run asynchronously using Redis.
* FastAPI used as the application server.
* Nginx used as a reverse proxy.
* Python ML workers receive jobs from Redis.

### Services
* Web server: Nginx
* Application server: FastAPI
* ML Workers: Python workers
* Message Queue: Redis
* Clientside: Sapper
* Docker-compose for the deployment of services.


### How do I get set up?

#### Run Project
```
cd MLtiplier
docker-compose build
docker-compose up
```

#### Build your ML worker
* Add your ML workload to run here backend_services/ml_worker/ml_worker/main.py
* ML job payload is added to Redis from the backend_services/app_server/app_server/main.py

#### Update your clientside
* Update ui/ directory to match the clientside required for Mltiplier

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* https://github.com/KshitijKarthick