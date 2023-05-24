# Twit-test
A twitter-like API.

## Documentation
The documentation for this API can be accessed [here](https://documenter.getpostman.com/view/20059082/UzBqp5wH)


## Technologies
- Python, Django, DRF
- Postgres
- Redis
- Docker

## Development

To run locally, type
```
docker-compose up --build
```
Ensure you include the env var in the .env.sample file.

*Keys prefixed with CLOUDINARY can be omitted.*

## Testing
To run tests, open a new console in the root directory and type
```
docker-compose exec web python manage.py test
```

## Deployment
The API was deployed on Heroku using Docker by building the Docker image using heroku.yml file

**Link:** https://twit-fleet.herokuapp.com

~~**NB:** I didn't configure Docker to serve static files hence the reason for the ugly look of the pages in web browser.
😐~~ See [issue #1](https://github.com/BOVAGE/Twit-test/issues/1)
