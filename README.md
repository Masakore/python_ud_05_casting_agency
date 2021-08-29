# python_ud_05_casting_agency
You are an Executive Producer within the company and are creating a system to simplify and streamline your process

### Installing Dependencies for the Backend

1. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

2. **PIP Dependencies** - install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```

3. **PostgreSQL** - install postgres on your local machine. Please refer to the [link](https://www.postgresql.org/download/)

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
createdb model_agency
psql model_agency < model_agency.sql
```

### Running the server
Ensure you are working using your created virtual environment. Go to the directory having app.py, 
To run the server, execute
```bash
python app.py
```

## API Reference

### Getting Started
- Base URL: This app can be run locally or through API hosted on Heroku. 
Local : `http://127.0.0.1:5000/`  
Heroku: `https://model-agency.herokuapp.com`
- Authentication: required. First, sign up through the following URL and  ask me to assign one of the roles below to get JWT.  

Sign up: [here](https://dev-ud-py.us.auth0.com/authorize?audience=model_agency&response_type=token&client_id=kJVEAXfaWlpChRAiSiLdKUiTDHNQHnfE&redirect_uri=https://127.0.0.1:8080/index)  

Roles: 
  - Casting Agent... can view all movies and actors
  - Casting Director... on top of Casting Agent permissions, can add, update and delete actors
  - Executive Producer... on top of Casting Director permissions, can add, update and delete movies

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 404: Resource Not Found
- 422: Not Processable 
- 500: Internal Server Error

Authorization related errors  
- 400: Invalid Claims or Invalid Header(see the description in reposnse)  
- 401: Invalid Header or Invalid Claims or Token Exired(see the description in response)  
- 403: Permission Not Found


### Endpoints 
#### GET /movies
- General:
    - Returns all available movies, success value.
- Sample: `curl http://127.0.0.1:5000/movies --header 'Authorization: Bearer <Your JWT>'`
``` 
{
  "movies": [
    {
      "id": 1,
      "title": "Kill Bill",
      "release_date": "2020-08-01 00:00:00"
    },
    {
      "id": 2,
      "title": "Snakes on a Plane",
      "release_date": "2000-08-01 00:00:00"
    }
  ], 
  "success": true
}
```

#### GET /actors
- General:
    - Returns all available actors, success value.
- Sample: `curl http://127.0.0.1:5000/actors --header 'Authorization: Bearer <Your JWT>'`
``` 
{
  "movies": [
    {
      "id": 1,
      "name": "Florence Pugh",
      "age": "25",
      "gender": "female"
    },
    {
      "id": 2,
      "name": "Arsenio Hall",
      "age": "65",
      "gender": "male"
    }
  ], 
  "success": true
}
```

#### POST /movies
- General:
    - This endpoint should take title and release date of a movie and register her in DB.
- Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <Your JWT>" -d '{"title":"Kill Bill", "release_date":"2020-01-01"}`

``` 
{
  "success": True
}
```

#### POST /actors
- General:
    - This endpoint should take an actor's name, age and gender and register her in DB.
- Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <Your JWT>" -d '{"name":"Anna May Wong", "age":100, "gender": "female"}`
``` 
{
  "success": True
}
```

#### PATCH /movies/{movie_id}
- General:
    - This endpoint updates existing movie with the value you pass and returns the updated movie in response.
- Sample: `curl http://127.0.0.1:5000/movies -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer <Your JWT>" -d '{"title":"Kill Bill", "release_date":"2020-01-01"}`

``` 
{
  "success": True,
  "movies": {
      "id": 1,
      "title": "Kill Bill",
      "release_date": "2020-08-01 00:00:00"}
}
```

#### PATCH /actors/{actors_id}
- General:
    - This endpoint updates existing movie with the value you pass and returns the updated actor in response.
- Sample: `curl http://127.0.0.1:5000/actors -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer <Your JWT>" -d '{"gender":"others"}`
``` 
{
  "success": True,
  "actor": {
      "id": 1,
      "name": "Florence Pugh",
      "age": "25",
      "gender": "others"}
}
```

#### DELETE /movies/{movie_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted actor, success value. 
- `curl -X DELETE http://127.0.0.1:5000/movies/1 -H "Authorization: Bearer <Your JWT>"`
```
{
  "delete": 1,
  "success": True
}
```

#### DELETE /actors/{actors_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted actor, success value. 
- `curl -X DELETE http://127.0.0.1:5000/actors/16 -H "Authorization: Bearer <Your JWT>"`
```
{
  "delete": 16,
  "success": True
}
```
