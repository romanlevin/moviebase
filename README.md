# MovieBase
## A toy Django 2.0 app

### Instructions
This project uses [Pipenv](https://github.com/pypa/pipenv). Run `$ pipenv install --dev` to install dependencies.

Create a file named `.env` in the projects root. It must define at least the following environment variables.
```bash
OMDB_API_KEY='XXXXXX'
DJANGO_SECRET_KEY='XXXXXXX'
```

You can obtain an OMDB API key [here](https://www.omdbapi.com/apikey.aspx).

You can override the default SQLite database by setting the `DATABASE_URL` environment variable to a database URL of your choice.

Run `$pipenv run pytest` to run tests.
