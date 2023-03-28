## 📰 Description
To be added


## :notebook_with_decorative_cover: Notes
- Did not utilize any Prompt Engineering technique
- Do not display the specific back-end error message to the front-end. Instead, provide user with three error options to identify the issue
```
There are three potential errors that may occur:
1. incorrect API key
2. rejection of request due to system safety protocols
3. high traffic on the system
```

## :building_construction: Environment

### :house: You should create a virtualenv
```
## Linux
make virtualenv


## Windows
python -m venv .venv
pip install -r requirements.txt
```


### :factory: How to activate the virtual environment
```
## Linux
source ./.env/bin/activate


## Windows
source ./.venv/Scripts/activate
```


### :house_with_garden: How to update the requirements
```
## Linux
make update-requirements-txt


## Windows
cmd.exe /C uninstall_install_requirements.bat
```


## :hammer: How to close a port that is already in use when trying to run it locally
```
sudo lsof -i :PORT_NUMBER
sudo kill PID
```


## :whale: Docker
#### How to run the multi-container application:
```
## RUN IT ON A SINGLE DOCKER HOST LOCALLY
docker-compose up -d # If the variable is not set, it defaults to stackdemo_local-network, which is the network used for local development
docker-compose logs -f --tail=100 --no-color

## DOWN
docker-compose down --volumes



## RUN IT ON A GROUP OF DOCKER HOSTS THAT ARE JOINED TOGETHER INTO A SINGLE VIRTUAL HOST (SWARM CLUSTER)
docker swarm init
docker service create --name registry --publish published=5000,target=5000 registry:2
export NETWORK_NAME=stackdemo_deployment-network
docker stack deploy --compose-file docker-compose.yml --with-registry-auth --orchestrator swarm mystack

## DOWN
docker stack rm mystack
docker service rm registry
docker swarm leave --force
```

#### Handy commands:
```
## PUSH THE GENERATED IMGS TO THE REGISTRY
docker-compose push

## OR DELETING ALL THE LOCAL IMGS
docker image rm $(docker image ls -a -q)

# OR REMOVING ALL RUNNING AND STOPPED CONTAINERS
docker rm -vf $(docker ps -aq)

## FIND THE CUSTOM NNETWORKS THAT YOU HAVE CREATED
docker network ls --filter type=custom
```


## 🛠 Initialization & Setup
    git clone https://github.com/pedroandreou/Gallery-of-Terror-Dreams.git


## :tophat: Author
<a href="https://www.linkedin.com/in/petrosandreou80/">
  <img align="center" src="https://img.shields.io/badge/Petros LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
</a>
