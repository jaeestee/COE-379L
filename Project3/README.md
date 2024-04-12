<h1 align="center">COE379L Project 3</h1>

This git repo contains the script ``api.py``. This script is a flask application that is used to predict whether a building is damaged or not. The data returned is explained in the sections below. An in-depth writeup about the project is located in the ``Project 3 Writeup.pdf`` file.

## Run Instructions

### Starting and Stopping the Inference Server
> Make sure that the repo is pulled before running everything!

Before starting the server, the user must mount the directory that contains all the images for testing with the ``docker-compose.yml`` file.

This is what the file looks like:
```
---
version: "3"

services:
    flask-app:
        build:
            context: ./
            dockerfile: ./Dockerfile
        ports:
            - 5000:5000
        image: jaeestee/ml-buildings-api:latest
        volumes:
            - ./config.yaml:/config.yaml
            #- ./cnn-split/test:/cnn-split/test # example
```
> An example is given in case the user does not have their own files at hand. Make sure to uncomment the line by removing the '#' before the '-'.

To start the server, run this command:
```
docker-compose up
```

> Pull the image manually if docker-compose isn't automatically pulling it!
> ```
> docker pull jaeestee/ml-buildings-api:latest
> ```

### Endpoints
|Route|Method|What it should do|
|---|---|---|
|``/models/buildings/v1``|GET|Gets information about the model.|
|``/models/buildings/v1``|POST|Using the model.|

There are two ways to make requests to the inference server once it is started:
1. Running it in a linux shell

To run in a linux shell use curl, for example:
```
curl http://172.17.0.1:5000/models/buildings/v1
```
> This is the GET method

Here is a sample of the POST method:
```
curl -X POST -H "Content-Type: application/json" -d '{"path": "cnn-split/test/damage/-93.722874_30.074742999999998.jpeg"}' http://172.17.0.1:5000/models/buildings/v1
```
> The ``-X POST -H "Content-Type: application/json" -d`` is CRUCIAL to make this all work! Also, make sure that the ``path`` value lines up with the volume mount that was created earlier!

2. Running a python script

Here are the python scripts:
```
import requests

rsp = requests.get("http://172.17.0.1:5000/models/buildings/v1")
rsp.json()
```
> The GET method. MAKE SURE TO IMPORT REQUESTS!

```
import requests

filename = '-93.722874_30.074742999999998.jpeg'
path = 'cnn-split/test/damage/' + filename

# make the POST request passing the single test case as the `path` field:
rsp = requests.post("http://172.17.0.1:5000/models/buildings/v1", json={"path": path})

# print the json response
rsp.json()
```
> The POST method. MAKE SURE TO IMPORT REQUESTS!

In both POST cases, you would input your own path to have the model predict if the image of the building is damaged or not.
