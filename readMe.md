**Interact ML DB Local Setup**

1. Download docker and table plus
2. Pull interact-ml main branch to the latest commit
3. create a .env file in the repo directory and paste this

```ENV = "development"

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "pgpass"
SSL_MODE = 'disable'

PORT = 3030
BACKEND_URL = "http://localhost:8000"

ML_URL = "http://localhost:3030"

LOGGER_URL = "http://localhost:8080"
LOGGER_SECRET = "-"
LOGGER_TOKEN = "-"

POPULATE = "FALSE"
```

1. Steps to run DB on docker and python locally **(recommended)**
- Change POPULATE = "TRUE" (in .env file) if u want to populate dummies
- Run the following commands
  1. pip install -r requirements.txt
  2. chmod +x ./build-container.sh
  3. ./build-container.sh -build
  4. python3 api.py

1. Steps to run both api and DB on docker 
- First Uncomment ml-api section in dev.docker-compose.yml file
- Run the following commands
  1. chmod +x ./build-container.sh
  2. ./build-container.sh -build (run ./build-container.sh -build -populate -> if u want to populate dummies)

Once setup just run your docker compose (either only db or both db and api) with the command: ./build-container.sh