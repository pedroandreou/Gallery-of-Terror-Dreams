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

or

source ./.venv/Scripts/activate
pip install -r unpinned_requirements.txt
echo "# Created automatically by make update-requirements-txt. Do not update manually!" > requirements.txt
pip freeze | grep -v pkg_resources >> requirements.txt
```


## 🛠 Initialization & Setup
    git clone https://github.com/pedroandreou/Gallery-of-Terror-Dreams.git
