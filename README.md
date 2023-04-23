# Project name 
joke-project

# Description
This project contains the BE squadmakers challenge

# Technologies
FastAPI - PostgreSQL

# Python version
Python 3.9.7

# How to run project
1. Go to /src folder by terminal
2. Create a virtual environment:  
python -m venv my-env
3. Activate a virtual environment:  
source /my-env/bin/activate
4. Install dependencies:  
pip install -r requirements.txt
5. Install postgreSQL. Open psql in the terminal and execute the following instructions:  
CREATE USER nombre_usuario WITH PASSWORD 'contraseña';  
CREATE DATABASE nombre_basedatos;  
GRANT ALL PRIVILEGES ON DATABASE nombre_basedatos TO nombre_usuario;  
CREATE TABLE jokes (
    id SERIAL PRIMARY KEY,
    joke_description TEXT NOT NULL
);

6. Create a .env file and add the credentials obtained in the last step.  
Same to .env.example
7. Run project:  
uvicorn app.route:app --reload
