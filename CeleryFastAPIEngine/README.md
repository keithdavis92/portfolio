# CeleryFastAPIEngine
## Tools Used
* Celery
* Redis
* FastAPI
* Swagger UI
* Dask

## Overview
This is a two endpoint API designed to take in a CSV file upload, process it, 
and return the results once the work has finished.

In this particular case, it is to process a CSV file that has real estate data
based on the number of sales within a specific district on a particular date.

It is highly likely that a number of real estate agents will be contributing to
the CSV file data, so there can be many records of sales that occur on the same date.

The goal of this engine is to take in the data and aggregate it so that we have the total
number of sales for a specific district, on a particular date.

 
## Initial Setup and Pre-requisites
Ensure you have Redis installed and running on your machine.
```sh
# Clone the repository
git clone git@github.com:keithdavis92/portfolio.git

cd portfolio/CeleryFastAPIEngine

# Create python virtual environment
python3 -m venv ./venv

source ./venv/bin/activate

pip install -r ./requirements.txt
```

## To Run
```sh
# In one terminal start Celery
cd portfolio/CeleryFastAPIEngine
celery -A main.celery worker --loglevel=info -Q submission

# Open another terminal, start the project
cd portfolio/CeleryFastAPIEngine
./venv/bin/python -m uvicorn main:app --reload
```
Now go to your chosen browser and paste in the link given in the terminal.
It should look like this:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Swagger UI should be open now. You will see two endpoints for POST and GET.

Go to `POST /submission/` and click the drop down arrow and click "Try it out"

Click "Choose File" and upload `CeleryFastAPIEngine/sample_files/upload_file.csv`

A task ID from celery will be returned. Navigate to the `GET` endpoint, click try it
out and paste in the task ID. 

You will then be able to download the processed file. 