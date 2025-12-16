## Bike Rental Forecasting System
**FastAPI**
It is used to develop an app

**Deployment Tools**
1. GitHub
2. Docker
3. Azure

**Deployment Steps**
1. Build the docker image of the source code
2. Push the docker image to container registry
3. Launch the web app server in the Azure
4. Pull the docker image from the container registry to web app server and run

## High Level Steps for Storing the Docker image/container in Azure cloud storage called ACR
1. Build Docker Image
2. Verify Image in the terminal
    1. docker images
3. ACR (Azure Container Registry) setup 
    1. Save the *Registry Name: lastbike*
    2. Registry Login Server name: *rentalregistry-c3hddphyaebuafar.azurecr.io*
    3. Registry Username: *lastbike*
    4. Docker image: bikerental

## Build image using Registry Login Server
1. docker build -t rentalregistry-c3hddphyaebuafar.azurecr.io/<image name>:latest .
2. docker login rentalregistry-c3hddphyaebuafar.azurecr.io
    1. Username: rentalregistry
    2. password: Xt+LR4AC9AIc3/EoMP4F
3. docker push rentalregistry-c3hddphyaebuafar.azurecr.io/<image name>:latest


## After  container registries created, Web app creation
4. Login to ACR:
    1. docker login <Registry Login Server name>.azurecr.io --username <registry-username>: Message -> Login Succeeded
    2. docker login lastbike-h5dueedddsduhybq.azurecr.io --username bikerental
5. Tag the image for ACR:
    1. Format::>>>>> docker tag <appsvc-tutorial-custom-image> <registry-name>.azurecr.io/<appsvc-tutorial-custom-image>:latest
    2. Implement::>>>>> docker tag bikerental lastbike-h5dueedddsduhybq.azurecr.io/bikerental:latest
6. Push the container into ACR:
    1. Format::>>>>>>> docker push <Registry Login Server name>.azurecr.io/<appsvc-tutorial-custom-image>:latest
    2. Implement::>>>>>>>> docker push bikerentalforecast.azurecr.io/bike-rental-app:latest
    3. Now your Docker image is in ACR(Azure Container Registry)

## Deploy the docker container from ACR to Azure Web App Service
1. First check actual registry name
    1. az acr list --output table


**Docker Imag, version and Tag**
1. Building docker image <Image Name>=bikerent
    1. docker build -t <image/base name>:latest .
    2. Tag Image with Correct Login Server: 
        1. Get the login server from *Azure Access Keys*: bikerent-edfgadexcec7gufg.azurecr.io
        2. az acr login --name <Image Name>: gives Login Succeeded message
        3. docker tag <Image Name>:latest 
        4. Format and use in below code: <Login Server>/<Image Name>:latest
        5. Finally: *docker tag bikerent:latest bikerent-edfgadexcec7gufg.azurecr.io/bikerent:latest*
    3. If required: az login (before push docker into ACR)
    


**Steps taken to build**
1. Create the Container registry in Azure Cloud.
    1. open Container registry
    2. give name of the group and other details
    3. create and review
    4. click on go to resources
    5. click on setting for Access Key
    6. copy *Login server*: bikerentforecast.azurecr.io
    7. checked the Admin box and copy the password provided by Azure.

2. *Web app for container*
    1. Give the same Resource Group name i created in container registry and all details
    2. For practice purpose choose free version and Click on next deployment and next docker container
    3. Container setups: single container, Azure container registry because i am going to push my image    here.
    4. Before the next in Azure cloud, quickly build the docker image in the machine.
    5. Once image pushed in the Azure cloud the web app is live 
3. *Continous Deployment/Integretion*
    1. As web app deploy in the Azure cloud then click on "Go to Resources"
    2. Go to Deployment -> Deployment Centre.
    3. click on Continous option
    4. click on "Github action: build and deploy manage your container app automatically with github action" and authorize linked github repo where Azure automatically create a yml file for github action.
    5. Save that file in Azure.
    6. Wait for fully deploy through github then go to azure depolyment centre overview to get my app link/url.




**Docker Login**
1. docker login
2. docker run hello-world (just for test whether docker is running or not)

**Commands to run on Terminal**
1. Build Docker image
    1. *docker build -t bikerentforecast.azurecr.io/bikeapp:latest .* 

2. Docker loging into Azure container registry url(bikerentforecast.azurecr.io) where i am going to push my image
    1. *docker login bikerentforecast.azurecr.io*
    2. Enter username: bikerentforecast
    3. Azure Password: EG+AN2pj8fhTNTz6D5krv4l

3. Docker push: after loging in azure registry requires to push that image in the Azure Container.
    1. *docker push bikerentforecast.azurecr.io/bikeapp:latest*

## Challenge in creating docker image 
1. Don't include libraries like random, os, pickle etc. in requirements.txt file.
2. In dockerfile include RUN pip install --upgrade pip 

## Azure web app challenge
1. Location region: west europe 
2. Free version to Basic

## Solve Github merge issue
1. git pull origin main --no-rebase
2. git push origin main

## Automatic 
- pip install pandas numpy matplotlib scikit-learn tensorflow
## Github issue
## Stop running docker
- Check how many docker container running : *docker ps*
- To stop all running container : *docker stop $(docker ps -q)*
- To stop just specific running docker : *docker stop <name specific container>*
- Running image to test: docker run -p 8000:8000 bikerental

## html localhost issue fixed
- while changing the port 8000 to 8080 throws me error although the url was working but not able to fetch the model prediction it was due to static hardcoded port on the index.html file and change <const API_URL = 'http://localhost:8000';> to <const API_URL = 'http://localhost:8080'>;


