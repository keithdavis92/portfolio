# FastAPIComplaintSystem
## Tools Used
* AWS SES
* AWS S3
* FastAPI
* Swagger UI
* Postgresql
* Alembic

## Overview
This is a complaint system designed through FastAPI. It creates an SQL database in order to store user information 
along with their respective complaints. Depending on the user (admin, approver, complainer), they will have certain
capabilities within this framework.

Complainers can log multiple complaints and each complaint has the option to upload a photo of the item they are not
happy with. The image will be processed and uploaded to AWS S3 for storage. 

The complaints default value are set to "Pending" until the Approver reviews them. They can then be approved or rejected.
If the item is approved, an email is sent to the user through AWS SES saying that their complaint has been approved.

## Initial Setup and Pre-requisites
```sh
# Clone the repository
git clone git@github.com:keithdavis92/portfolio.git

cd portfolio/FastAPIComplaintSystem

# Create python virtual environment
python3 -m venv ./venv

source ./venv/bin/activate

pip install -r ./requirements.txt
```

## To Run
First you will need to create a superuser so that you know the relevant credentials to log in.
You will then also have full access to all endpoints and can easily explore the project. 

This is done through the ```create_super_user.py``` script at the top level of the project. You can fill in the details
with a username of your choice:
```sh
# In a bash terminal, execute the following
cd portfolio/FastAPIComplaintSystem
export PYTHONPATH=./
python commands/create_super_user.py -f <first_name> -l <last_name> -e <email> -p <phone> -i <iban> -pa <password>
```

Then you can start the app:
```sh
# In a terminal, start the project
cd portfolio/FastAPIComplaintSystem
./venv/bin/python -m uvicorn main:app --reload
```

Now go to your chosen browser and paste in the link given in the terminal.
It should look like this:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Swagger UI should be open now. You will see a list of endpoints.

You can then register some users through the API. 

Once a user is registered, you will retrieve the token ID. You can copy this and use it to log in as the user
so as to log a complaint. Click "Authorise" at the top right of Swagger and paste in the key.

You are now logged in as the user and can log a complaint. If you wish to attach a photo, you will need to first
encode it into base64, and then paste that into the JSON POST.

Once a complaint has been logged, you could create another user called approver. This can be done through the 
API rather than running the script. Once you register the user, you can make the user an approver when you log
in as the superuser. 

As an approver, you can obtain the list of complaints and run a PUT on the complaint ID in order to either approve
or reject the complaint.
