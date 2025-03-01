# Performa Server

## dependency
python@3.13.2

## database
mysql@9.2.0

way to start mysql server in docker
```shell
$ cd docker/
$ docker-compose up -d 
```

**OR YOU CAN JUST USE YOUR LOCAL MYSQL SERVER, edit DB_URI in config.py**


## server install 
- MacOS
```shell
$ cd server
$ python -m venv venv
$ . venv/bin/activate
(venv)$ pip install -r requirements.txt
```
- Windows
```shell
$ Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
$ cd server
$ py -3 -m venv venv
$ venv\Scripts\activate
(venv)$ py -m pip install -r requirements.txt
```

## server start

---------------

FIRST RUN:

if you first run this server, you should edit the config.py#L16.

change FIRST_RUN = True, to init the database, and DO NOT submit this file.

when the server started, you can change FIRST_RUN = False back.

---------------
 

- MacOS
```shell
(venv)$ start.sh
```

- Windows
```shell
(venv)$ start.bat
```

- IDE

**OR YOU CAN JUST RUN performa.py in YOUR IDE**


---------------

## Login Test

```shell
## request send-otp
curl --location 'http://127.0.0.1:5001/api/send-otp' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "cchen7166@conestogac.on.ca"
}'
## response send-otp
{
  "code": 200,
  "data": "ok",
  "success": true
}
## server print
cchen7166@conestogac.on.ca SEND_OTP_SUBJECT OTP: 903916

###########################

## request login
curl --location 'http://127.0.0.1:5001/api/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "cchen7166@conestogac.on.ca",
    "otp": 903916
}'
## response login
{
  "code": 200,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6ImNjaGVuNzE2NkBjb25lc3RvZ2FjLm9uLmNhIiwicm9sZV9pZCI6MSwicm9sZV9uYW1lIjoiU1RVREVOVCIsImV4cCI6MTc0MDg1NDE1MH0.ti1U2g-JxRKdXrOr4NJ473MxQf-dJxYiuUW4xCXkMLg"
  },
  "success": true
}

###########################

## Request test_auth
curl --location 'http://127.0.0.1:5001/api/test_auth' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6ImNjaGVuNzE2NkBjb25lc3RvZ2FjLm9uLmNhIiwicm9sZV9pZCI6MSwicm9sZV9uYW1lIjoiU1RVREVOVCIsImV4cCI6MTc0MDg1NDE1MH0.ti1U2g-JxRKdXrOr4NJ473MxQf-dJxYiuUW4xCXkMLg'

## Response test_auth
{
  "code": 200,
  "data": {
    "email": "cchen7166@conestogac.on.ca",
    "exp": 1740854150,
    "role_id": 1,
    "role_name": "STUDENT",
    "user_id": 1
  },
  "success": true
}
```