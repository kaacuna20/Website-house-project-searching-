<div class="row ">
	<div class="col ">
		<h1  style="color:#C6AB7C; font-size: 80px; font-weight:bold;">HOUSE FINDER</h1>
	</div>
</div>

<h4 align="justify">In the Atlantico department - Colombia, there are many housing projects, of many types (VIS, VIP, NO VIS) where people of all classes can get their own home, but there are many options and I thought the following, why not create a website where people can search all options in one site instead to do it website by website? I decided start to create my first big project, using my knowlegde of HTML, CSS, Bootstrap, Python and two of its frameworks, FastApi and Flask and last, conect all this using docker containers.</h4> 

### Features of aplication

- Let view housing projects in Atlantico - Colombia, specifically in Puerto Colombia, Barranquilla and Soledad city, filter the search by construction company, location and city;
- User can register and login section, personalize their profiles and save their favorites projects on their accounts;
- got the option to change their passwords or get a new password in section forgot password where the new password is sent to their email;
- Each project page there is a comment section where each user can leave their opinions about the project;
- There is a section for developer where can read the documentation about the API, whatching the routes to make the requests, the differents responses and restrictions;
- Developers can generate their apikey to be allowed making requests;

### Dockerized  House Finder

This project is a Dockerized setup for the House Finder application, consisting of multiple services: a Flask web application, a FastAPI API, an NGINX reverse proxy, and a PostgreSQL database. The services are defined in a `docker-compose.yml` file for easy orchestration and deployment.

## Table of Contents
- [Project Structure](#Project-Structure)
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Services](#services)
  - [webapp_house_finder](#webapp_house_finder)
  - [api_house_finder](#api_house_finder)
  - [nginx](#nginx)
  - [postgresql_db](#postgresql_db)
- [Networks](#networks)
- [Volumes](#volumes)
- [Testing app services](#Testing-app-services)
- [Running the Application](#running-the-application)
- [Diagram](#diagram)

## Project Structure
```ini
Website-house-project-searching/
├── images/
│   ├── api/
│   └── profile/
├── postgresql_db/
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf
├── api-house-finder/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── run.py
│   └── app/
│      ├── __init__.py
│      ├── database.py
│      ├── main.py
│      ├── models.py
│      ├── helper/
│      │     ├── download_img.py
│      │     └── normalize_text.py
│      ├── routers/	
│      │  ├── __init__.py
│      │  └── projects.py
│      ├── utils/	
│      │  ├── __init__.py
│      │  └── auth.py
│      └── test_project.py
│
├── webapp-house-finder/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── run.py
|   ├── config.py
│   └── app/
│      ├── __init__.py
│      ├── models.py
│      ├── auth/
│      │     ├── __init__.py
│      │     └── forms.py
|      ├── common/
│      │     ├── __init__.py
│      │     └── mail.py
│      ├── routers/	
│      │   ├── __init__.py
|      │   ├── api_documentation.py
|      │   ├── api.py
|      │   ├── index.py
|      │   ├── profile.py
|      │   ├── user.py
│      │   └── project.py
|      ├── templates/
|      ├── static/
│      ├── utils/	
│      │  ├── __init__.py
│      │  └── helpers.py
│      └── test/
|         ├── __init__.py
|         ├── conftest.py
|         ├── test_api_route.py
|         ├── test_profile_route.py
|         └── test_user_route.py
│   
├── docker-compose.png  
├── docker-compose.yml
└── .env

```

## Overview

This setup uses Docker Compose to manage the following services:

1. **Flask Web Application** (`webapp_house_finder`)
2. **FastAPI API** (`api_house_finder`)
3. **NGINX Reverse Proxy** (`nginx`)
4. **PostgreSQL Database** (`postgresql_db`)

All services are connected via a custom Docker network called `house_finder_web`.

## Prerequisites

- Docker installed on your machine
- Docker Compose installed on your machine
- Environment variables set in a `.env` file
- Graphviz installed and configured (for generating diagrams)


## Configuration

Create a `.env` file in the root directory of your project with the following variables:

```ini
# .env file
PRO_DB_URL=your_database_url
SECRET_APP_KEY=your_secret_key
FLASK_APP=your_flask_app
PRO_CONFIGURATION_SETUP=your_configuration_setup
APP_PASSWORD_EMAIL=your_app_password_email
ADMINISTER_EMAIL=your_admin_email
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_USER=your_postgres_user
POSTGRES_DB=your_postgres_db
```
## Services
### webapp_house_finder

- Description: This service runs the Flask web application.
- Build Context: `./webapp-house-finder`
- Dockerfile: `Dockerfile`
- Container Name: `flask_house_finder`
- Ports: `5003:5003`
- Volumes:
     - `./images/api:/app/app/static/images/img-projects`
     - `./images/profile:/app/app/static/images/img-profile`
- Environment Variables:
     - `DB_URL`
     - `SECRET_APP_KEY`
     - `FLASK_APP`
     - `CONFIGURATION_SETUP`
     - `APP_PASSWORD_EMAIL`
     - `ADMINISTER_EMAIL`
     - `DEBUG=False`
- Dependencies: `postgresql_db`
- Network: `house_finder_web`

The Dockerfile configuration is the next:
```init
FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y locales && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen en_US.UTF-8

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

RUN pip install pytest

COPY . .

EXPOSE 5003

CMD ["gunicorn", "run:app", "-w", "4", "--bind", "0.0.0.0:5003"]
```
  
### api_house_finder
- Description: This service runs the FastAPI application.
- Build Context: `./api-house-finder`
- Dockerfile: `Dockerfile`
- Container Name: `fastapi_house_finder`
- Ports: `8000:8000`
- Volumes:
     - `./images/api:/app/app/static/images/img-projects`
- Environment Variables:
     - `DB_URL`
     - `SECRET_APP_KEY`
- Dependencies: `postgresql_db`
- Network: `house_finder_web`
The Dockerfile configuration is the next:
```init
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip install pytest

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### nginx
- Description: This service runs the NGINX reverse proxy.
- Build Context: `./nginx`
- Ports: `80:80`
- Dependencies: `webapp_house_finder`, `api_house_finder`
- Network: `house_finder_web`
The Dockerfile configuration is the next:

```init
FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
```

### postgresql_db
- Description: This service runs the PostgreSQL database.
- Image: `postgres:12`
- Container Name: `postgresql_db`
- Ports: `5432:5432`
- Environment Variables:
     - `POSTGRES_PASSWORD`
     - `POSTGRES_USER`
     - `POSTGRES_DB`
- Volumes:
     - `./postgresql_data:/var/lib/postgresql/data`
- Network:
     - `house_finder_web`

## Networks
- house_finder_web: A custom network for connecting all the services.

## Volumes
- postgresql-data: Stores PostgreSQL data.
- images: Stores images used by the applications.

## Testing app services
In same `.env` file in the root directory of your project with the following test variables:
```ini
# .env file
TEST_CONFIGURATION_SETUP=TEST_CONFIG_FLASKAPP
TEST_DB_URL=SQLITE_URL_TESTING
TEST_APIKEY=TEST_CREDENTIALS_APIKEY
TEST_TOKEN=TEST_CREDENTIALS_TOKENSECRET
```
Docker compose configuration we add the next:

```ini
  test_fastapi:
    build:
      context: ./api-house-finder
      dockerfile: Dockerfile
    command: ["pytest"]
    environment:
      - DB_URL=${TEST_DB_URL}
      - TEST_APIKEY=${TEST_APIKEY}
      - TEST_TOKEN=${TEST_TOKEN}
    depends_on:
      - postgresql_db
    env_file:
      - .env

  test_flask:
    build:
      context: ./webapp-house-finder
      dockerfile: Dockerfile
    command: ["pytest", "app/tests/"]
    environment:
      - TEST_CONFIGURATION_SETUP=${TEST_CONFIGURATION_SETUP}
    env_file:
      - .env

```

## Running the Application

1. Ensure Docker and Docker Compose are installed.

2. Create a .env file in the root directory with the necessary environment variables.

3. Run the following command to build and start all services:
   
   `docker-compose up --build`
4. Access the services:

- Flask Web Application: http://localhost:5003
- FastAPI API: http://localhost:8000
- NGINX Reverse Proxy: http://localhost:80

5. To stop the services, run:

   `docker-compose down`

## Diagram
- Below is a visual representation of the Docker Compose setup:

![Docker Compose Diagram](docker-compose.png)
