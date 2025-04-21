# proyectoCBD
# Installation guide
Please go to this web page to install Neo4j depending on the OS: https://neo4j.com/docs/operations-manual/current/installation

Create a virtual environment in the root folder of the entire project and activate it:
```
python -m venv venv
source venv/bin/activate # If you are on Linux
.\venv\Scripts\activate # If you are on Windows 
```

Install dependencies:
```
pip install -r requirements.txt
```

Run the project:
```
python manage.py runserver
```