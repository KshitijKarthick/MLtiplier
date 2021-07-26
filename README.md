# MLtiplier

A template repository for serving ML applications.
The service runs as an async ML job runner, providing job id's to the client for the submitted ML task.
The web-server used is Nginx, app-server is fastAPI, redis is a queue-manager.

### Services

#### Web server

Nginx is used to serve static content from clientside.
The service also forwards the /api requests to the API server.

#### App server

FastAPI is the application server which recieves /api calls.
It runs async ML tasks using a queue.
It provides the clientside with a job id and submits the job to the ML worker.
The clientside can then poll for the status of the job result.

#### Queue

Redis is used as the queue to make the entire process Async with the client.
This helps control the number of ML tasks in execution since they are memory and CPU intensive.

#### Clientside

The clientside which submits jobs and polls for jobs results. 

### How do I get set up? ###

```
docker-compose build
docker-compose up
```

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines
