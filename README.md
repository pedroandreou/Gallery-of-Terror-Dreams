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


### Make a copy of the example environment variables file (this is not the virtual env; don't get confused; it's just for keeping your api-key secured)
```
## Linux
cp .env_vars.example .env_vars


## Windows
xcopy .env_vars.example .env_vars
```


### How to activate the virtual environment to run the code
```
## Linux
source ./.env/bin/activate


## Windows
source ./.venv/Scripts/activate
cmd.exe /C update_requirements.bat
```


## How to run the two containers under the same network:
```
./build-and-run.sh
```


## 🛠 Initialization & Setup
    git clone https://github.com/pedroandreou/Gallery-of-Terror-Dreams.git
