## 📰 Description
To be added


## :building_construction: Environment

### :house: You should create a virtualenv
```
## Linux
make virtualenv


## Windows
python -m venv .venv
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
make update-requirements-txt (For reproducibility)


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
## RUN LOCALLY
docker-compose up -d --build --no-cache # If the variable is not set, it defaults to stackdemo_local-network, which is the network used for local development


## DEPLOYMENT
export NETWORK_NAME=stackdemo_deployment-network
docker stack deploy --compose-file docker-compose.yml --with-registry-auth --orchestrator swarm mystack
```

#### Handy commands:
```
## UP
docker-compose up -d --build --no-cache
docker-compose logs -f --tail=100 --no-color


## DOWN
docker-compose down


## OPTIONAL FOR REBUILDING THE IMAGES
docker-compose build


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
