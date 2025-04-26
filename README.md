# proyectoCBD
# Installation guide
Please go to this web page to install Neo4j depending on the OS: https://neo4j.com/docs/operations-manual/current/installation
Attention: this guide is made based on a work environment in Linux; the steps for Windows may vary.

First, you must clone this repo:
```
git clone https://github.com/claudiocortescarrasco/proyectoCBD.git # If you use HTTP
git clone git@github.com:claudiocortescarrasco/proyectoCBD.git # If you use SSH
```

Create a virtual environment in the root folder of the entire project and activate it:
```
cd proyectoCBD/appCBD
python -m venv venv
source venv/bin/activate # If you are on Linux
.\venv\Scripts\activate # If you are on Windows 
```

Install dependencies:
```
pip install -r requirements.txt
```
To activate de Neo4j service, do:
```
sudo systemctl start neo4j
```

The database browser is available in `http://localhost:7474/browser`

Run the project:
```
python manage.py runserver
```

To load the data manually in the database you can use this command (you can do this in the app):
```
python manage.py cargar_datos
```
