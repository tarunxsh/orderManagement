# Order Management System

create dev directory
```
mkdir dev
cd dev
```
Clone project in current directory
```
git clone https://github.com/tarunesh1234/orderManagement.git
```

dev\
|-- orderManagement


###### open two terminals in current directory and setup environment
## Setup Environment

```
python3 -m venv env
```
dev\
|-- env\
|-- orderManagement

## Activate Environment

```
source env/bin/activate
```
## Install Requirements
go to orderManagement Directory [project root]
```
pip install -r requirements.txt
```
## Run project

### Run project in one terminal

Migrate model
```
python3 manage.py makemigrations
python3 manage.py migrate
``` 
Create superuser
```
python3 manage.py createsuperuser
```
Run server
```
python3 manage.py runserver
```

Run celery in second terminal

```
celery -A orderManagement worker -B --concurrency=1 --loglevel=info
```

## Populate Delivery boy database
* Use superuser password to login to [admin](/admin) panel
* Go to Dboys database
* Add required no. Dboys (Name only) 

## Placing Order
* open [simulator](/) web page in web browser
* place order

![This is simulator web page.](/images/simulatorWebpage.png "simulator webpage.")
**log files** will be generated in logs directory  located in project root directory


## Note
1. ***Server can't handle order more than no. of Dboys availabe at a time***
2. ***If placed more order than no. of Dboys, receive them manualy from simulator page***\

### WIP
1. Dockerization

## Images
![This is celerey screen.](/images/celery.png "celerey screen.")\
![This is first log file.](/images/firstlog.png "first log file.")\
![This is second log file](/images/secondlog.png "second log file.")\

