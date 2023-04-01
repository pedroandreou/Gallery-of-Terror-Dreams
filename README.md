<h1 align="center" style="color:red;">Gallery of Terror Dreamms</h1>


## 📰 Description
Introducing Terror Dreams 😱🔪 - an app that masterfully weaves the chilling essence of Texas Chainsaw-style horror with the spine-tingling soundtrack of The Exorcist. Drawing inspiration from the 2003 Texas Chainsaw Massacre Official Trailer #1 (at 1:19) 🎬 and the eerie, iconic Exorcist music 🎶, this app transforms ordinary text into a blood-curdling, heart-pounding experience 💀.

Terror Dreams takes artistic liberties to craft a cinematic horror experience that captures your attention and enhances your senses 👻. With this app, you can now conjure the bone-chilling atmosphere of classic horror films right on your device 📱, giving you the power to share the thrill with friends or keep it all to yourself 🤫.

Dare to enter the gallery of Terror Dreams, where your text takes on a sinister new life 🌑 and the line between reality and nightmare blurs 😨. Are you brave enough to embrace the darkness within? 🖤

<p align="center">
<img src="https://j.gifs.com/79BM9O.gif" alt="Your Image Description" width="1200" height="600" />
</p>
[Click here to view the GIF with sound](https://gifs.com/embed/gallery-of-terror-dreams-79BM9O?muted=false)

<blockquote>
PS: Architecture: Semi-Modular/Organized Monolithic
</blockquote>


## :notebook_with_decorative_cover: Notes
- Did not utilize any Prompt Engineering technique :sleeping:
- Probs had to find a way to separate the requirements for each service as each image is built out of all the requirements :sleeping:


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
pip install -r requirements.txt
```


### :house_with_garden: How to update the requirements
```
## Linux
make update-requirements-txt


## Windows
cmd.exe /C update_requirements.bat
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

## FIND THE CUSTOM NNETWORKS THAT YOU HAVE CREATED
docker network ls --filter type=custom
```


## 🛠 Initialization & Setup
    git clone https://github.com/pedroandreou/Gallery-of-Terror-Dreams.git


## :scroll: License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.


## :tophat: Author
<a href="https://www.linkedin.com/in/petrosandreou80/">
  <img align="center" src="https://img.shields.io/badge/Petros LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
</a>
