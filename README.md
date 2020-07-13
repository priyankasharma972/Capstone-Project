## STAR-CASTING-AGENCY
This casting agency models a company which is responsible for creating movies and managing actors by assigning movies to them.

This Application is hosted on Heroku:
https://star-casting-agency.herokuapp.com/


## Motivation
This is the final project for Udacity FSND

## Dependencies
These are listed in `requirements.txt`
It can be installed with `pip install -r requirments.txt`

## Authentication
This Agency has 3 registered users:

1. Casting-Assistant:
    Can view actors and movies
2. Casting-Director:
    All permissions a Casting Assistant has
    Add or delete an actor from the database
    Modify actors or movies
3. Executive-Producer:
    All permissions a Casting Director has
    Add or delete a movie from the database

The Authentication is carried out by third-party authentication tool which is `Auth0`
The Auth0 domain and api audience can be found in `setup.sh`.


## End-Points
### `GET /movies`
This end point will fetch all movies from database.
sample:
{
  "movies": [
    {
      "id": 1,
      "release_date": 13,
      "title": "Dark"
    },
    {
      "id": 4,
      "release_date": 13,
      "title": "NewMovie"
    },
    {
      "id": 6,
      "release_date": 78,
      "title": "test"
    }
  ],
  "success": true
}

### `POST /movies`
This end point is used to post a new movie.
sample:
Data:
json={"title": "Dark", "release_date":"78"}
Response:
{
  "movie": "Dark",
  "success": true
}

### `PATCH /movies/<int:id>`
This end point updated the details in an existing movie
sample:
Data:
json={"title": "Sky", "release_date":"78"}
Response:
{
  "movie": {
    "id": 3,
    "release_date": 78,
    "title": "Sky"
  },
  "success": true
}

### `DELETE /movies/<int:id>`
This end point deletes a movie from the database
sample:
{
  "delete": 3,
  "success": true
}

### `GET /actors`
This end point will get all actors from the database
sample:
{
  "actors": [
    {
      "gender": "Female",
      "id": 1,
      "name": "Martha"
    },
    {
      "gender": "Male",
      "id": 2,
      "name": "Jonas"
    }
  ],
  "success": true
}

### `POST /actors`
This end point will post a new actor
sample:
Data: json= {"name":"Claudia", "gender":"Female"}
Response:
{
  "actor": "Claudia",
  "success": true
}

### `PATCH /actors/<int:id>`
This end point updates the details of an existing actor
sample:
Data: Json={"name":"Tiedmann", "gender":"Female"}
Response:
{
  "actor": {
    "gender": "Female",
    "id": 3,
    "name": "Tiedmann"
  },
  "success": true
}

### `DELETE /actors/<int:id>`
This end point will delete an existing actor
sample:
{
  "delete": 3,
  "success": true
}

## Tests
To run the tests, use `test_app.py` with below command:
`python test_app.py`

## Author
Priyanka Sharma authored this API with only backend features present in `flaskr`, `test_app.py` and `database` folders. 
Authentication can be found in `auth` folder.


