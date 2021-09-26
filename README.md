# COVID Futures

Predictions about Australia's COVID future.


## Getting Started

Install pipenv:

```
pip install pipenv
```

Install dependencies (both Python and JS):

```
pipenv install
npm install
```

Build assets:

```
npm run webpack:dev
# or
npm run webpack:prod
```

Configure the database (for development and testing):

```
echo "export COVID_FUTURES_DATABASE_URI_TEST='mysql+pymysql://covid_futures:covid_futures@localhost/covid_futures_test'" >> .env
echo "export COVID_FUTURES_DATABASE_URI='mysql+pymysql://covid_futures:covid_futures@localhost/covid_futures_dev'" >> .env
```

```
pipenv run load-schema
pipenv run ingest-data
```

Run the development server:

```
pipenv run server
```

Run tests:

```
pipenv run test
# or
pipenv run test-watch
```


## Training

To train the model from scratch:

```
pipenv run train-model
```


## Making predictions

Run inference and save predictions to the database:

```
pipenv run predict
```


## Deployment

The production database URL is configured via the `COVID_FUTURES_DATABASE_URI` environment variable. For
instructions for PythonAnywhere hosting, see:

https://help.pythonanywhere.com/pages/environment-variables-for-web-apps/

To initialise a production database:

```
pipenv run load-schema
pipenv run ingest-data
```


## Licence

Copyright Rohan Mitchell, released under GPL v3 licence.
