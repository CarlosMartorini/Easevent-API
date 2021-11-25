# Easevent <img src='icon.png' width='50px' title='Easevent'>

API developed in Django, for non-profit application, which provides a layout so that there is the possibility of making the connection between small musical artists with establishments and their owners, aiming to establish partnerships with regularities on event dates.

# Clone

Clone this repository on your local machine. 

Use the terminal for this.

```bash
git clone git@gitlab.com:lucirasilva/easy-event.git
```

# Installation

Enter the project dependencies and install the virtual environment.

```bash
python -m venv venv
```

Enter the virtual environment

```bash
source venv/bin/activate
```

And now install the dependencies stored in the requirements.txt file

```bash
pip install -r requirements.txt
```
# Usage

Run migrations with the following command so that db.sqlite is created.

```bash
python manage.py migrate
```

Put the local server to run.

```bash
python manage.py runserver
```

Local server URL: http://127.0.0.1:8000/

# Routes

## Create User Artist

- POST api/users/
- Status HTTP 201 CREATED

```json
{
    "username": "John",
    "password": "123456",
    "email": "john@gmail.com",
    "is_superuser": false,
    "phone": "199898989",
    "solo": false,
    "hour_price": 150.00
}
```
- Expected response

```json
{
    "id": 1,
    "username": "John",
    "password": "123456",
    "email": "john@gmail.com",
    "is_superuser": false,
    "phone": "199898989",
    "solo": false,
    "hour_price": 150.00
}
```

- If there is an attempt to create a username who is already registered.
- Status HTTP 409 CONFLICT.

```json
{
    "error": "User already exists!"
}
```

## Create User Owner

- POST api/users/
- Status HTTP 201 CREATED

```json
{
    "username": "Doe",
    "password": "67890",
    "email": "doe@gmail.com",
    "is_superuser": true,
    "phone": "119797979",
}
```
- Expected response

```json
{
    "id": 2,
    "username": "Doe",
    "password": "67890",
    "email": "doe@gmail.com",
    "is_superuser": true,
    "phone": "119797979",
}
```

- If there is an attempt to create a username who is already registered.
- Status HTTP 409 CONFLICT.

```json
{
    "error": "User already exists!"
}
```

## Login

- POST api/login/
- Status HTTP 200 OK

```json
{
  "username": "John",
  "password": "123456"
}
```

- Expected response

```json
{
  "token": "dfd384673e9127213de6116ca33257ce4aa203cf"
}
```

- If you try to give wrong information
- Status HTTP 401 UNAUTHORIZED

```json
{
    "error": "Username or password may be wrong!"
}
```

- If any information is missing
- Status HTTP 406 NOT ACCEPTABLE

```json
{
    "error": "username or password it's missing"
}
```

## Invalid token

- All endpoints that require the use of an access token must respond as follows if an invalid token is entered
- Status HTTP 401 UNAUTHORIZED

```json
// REQUEST
// Header -> Authorization: Token <invalid-token>
```

```json
{
    "detail": "Invalid token."
}
```

- If a valid token is entered but does not meet the minimum permission requirements
- Status HTTP 403 FORBIDDEN

```json
// REQUEST
// Header -> Authorization: Token <forbidden-token>
```

```json
{
    "detail": "You do not have permission to perform this action."
}
```

## Create Event

- POST api/events
- Status HTTP 200 OK
> The event lineup will be included soon. 

```json
{
    "date": "",
    "repeat_date": "",
    "address_id": {
        "street": "W Pine St",
        "neighbourhood": "Downtown Orlando",
        "number": 37,
        "city": "Orlando",
        "state": "Florida",
    },
    "owner_id": 2,
    "details": "Some details for local event",
    "base_price": 120.00,
    "music_styles": [
        {
            "name": "Rock"
        },
        {
            "name": "Country"
        }
    ]
}
```

- Expected response

```json
{
    "id": 1,
    "date": "",
    "repeat_date": "",
    "address_id": {
        "street": "W Pine St",
        "neighbourhood": "Downtown Orlando",
        "number": 37,
        "city": "Orlando",
        "state": "Florida",
    },
    "owner_id": 2,
    "details": "Some details for local event",
    "base_price": 120.00,
    "music_styles": [
        {
            "name": "Rock"
        },
        {
            "name": "Country"
        }
    ]
}
```

- If any required information is missing
- Status HTTP 406 NOT ACCEPTABLE

```json
{
    "error": "Date it's missing"
}
```

## Include Artists on Event Lineup

- PUT api/events/1
- Status HTTP 200 OK

```json
{
    "lineup": [
        {
            "artist_id": 1,
            "performance_datetime": ""
        },
        {
            "artist_id": 3,
            "performance_datetime": ""
        }
    ]
}
```

- Expected response

```json
{
    "id": 1,
    "date": "",
    "repeat_date": "",
    "address_id": {
        "street": "W Pine St",
        "neighbourhood": "Downtown Orlando",
        "number": 37,
        "city": "Orlando",
        "state": "Florida",
    },
    "owner_id": 2,
    "details": "Some details for local event",
    "base_price": 120.00,
    "music_styles": [
        {
            "name": "Rock"
        },
        {
            "name": "Country"
        }
    ],
    "lineups": [
        {
            "artist_id": 1,
            "performance_datetime": ""
        },
        {
            "artist_id": 3,
            "performance_datetime": ""
        }
    ]
}
```

- If you try to update a non-existent event
- Status HTTP 404 NOT FOUND

```json
{
    "error": "Event not founded!"
}
```

- If you try to pass an id that is a owner **is_superuser=true**
- Status HTTP 400 BAD REQUEST

```json
{
    "error": "Only artists can be enrolled in the lineups events."
}
```

- If you try to include artists on a non-existent event
- Status HTTP 404 NOT FOUND

```json
{
    "error": "Invalid event_id."
}
```

- If you try to pass a artist_id that doesn't exist
- Status HTTP 404 NOT FOUND

```json
{
    "error": "Invalid artist_id."
}
```

## Showing all Events

- GET api/events
- Status HTTP 200 OK

```json
{
    "id": 1,
    "date": "",
    "repeat_date": "",
    "address_id": {
        "street": "W Pine St",
        "neighbourhood": "Downtown Orlando",
        "number": 37,
        "city": "Orlando",
        "state": "Florida",
    },
    "owner_id": 2,
    "details": "Some details for local event",
    "base_price": 120.00,
    "music_styles": [
        {
            "name": "Rock"
        },
        {
            "name": "Country"
        }
    ],
    "lineups": [
        {
            "artist_id": 1,
            "performance_datetime": ""
        },
        {
            "artist_id": 3,
            "performance_datetime": ""
        }
    ]
},
{
    "id": 2,
    "date": "",
    "repeat_date": "",
    "address_id": {
        "street": "2nd Ave",
        "neighbourhood": "Rose Hill",
        "number": 519,
        "city": "New York",
        "state": "New York",
    },
    "owner_id": 4,
    "details": "Some details for local event",
    "base_price": 100.00,
    "music_styles": [
        {
            "name": "Rock"
        },
        {
            "name": "Country"
        },
        {
            "name": "House"
        }
    ],
    "lineups": [
        {
            "artist_id": 1,
            "performance_datetime": ""
        },
        {
            "artist_id": 3,
            "performance_datetime": ""
        },
        {
            "artist_id": 5,
            "performance_datetime": ""
        }
    ]
}
```

## Delete Event

- DELETE api/events/1
- Status HTTP 204 NO CONTENT
- Expected response

```json
// RESPONSE STATUS -> HTTP 204 NO CONTENT
```

- If you try to delete a non-existent course
- Status HTTP 404 NOT FOUND

```json
{
    "error": "Event not founded."
}
```