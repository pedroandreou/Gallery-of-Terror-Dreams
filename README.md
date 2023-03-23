## 📰 Description
To be added



## :building_construction: Environment

### You should create a virtualenv with the required dependencies by running
```
## Linux
make virtualenv


## Windows
python -m venv .venv
```


### How to activate the virtual environment to run the code
```
## Linux
source ./.env/bin/activate
make update-requirements-txt (For reproducibility)


## Windows
source ./.venv/Scripts/activate
cmd.exe /C uninstall_install_requirements.bat
```


## How to run the two containers under the same network:
```
./build-and-run.sh
```


## How to close a port that is already in use when trying to run it locally
```
sudo lsof -i :PORT_NUMBER
sudo kill PID
```


## :whale: Docker
```
## UP
docker-compose up -d
docker-compose logs -f --tail=100 --no-color

## DOWN
docker-compose down
```


## 🛠 Initialization & Setup
    git clone https://github.com/pedroandreou/Gallery-of-Terror-Dreams.git


## :tophat: Author
<a href="https://www.linkedin.com/in/petrosandreou80/">
  <img align="center" src="https://img.shields.io/badge/Petros LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
</a>
