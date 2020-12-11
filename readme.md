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

Run project in one terminal

```
python3 manage.py runserver
```

Run celery in second terminal

```
celery -A orderManagement worker --concurrency=1 --loglevel=info
```


## Placing Order
open simulator web page order.html in web browser\
place order\
![This is simulator web page.](/images/simulatorWebpage.png "simulator webpage.")
**log files** will be generated in logs directory  located in project root directory


**Note** Server can't handle more than 3 order at a time 

## Images
![This is celerey screen.](/images/celery.png "celerey screen.")\
![This is first log file.](/images/firstlog.png "first log file.")\
![This is second log file](/images/secondlog.png "second log file.")\

