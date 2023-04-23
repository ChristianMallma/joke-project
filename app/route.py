import yaml

from fastapi import FastAPI
from jokes.entrypoint import jokes


# Load YAML file
with open("configuration/jokes.yaml") as file:
    spec = yaml.load(file, Loader=yaml.FullLoader)


app = FastAPI(openapi_spec=spec,
              title='Joke Project',
              version='1.0.0')

app.include_router(jokes.router)


@app.get("/openapi.yaml", tags=['Documentation'])
def get_open_api_endpoint():
    return spec
