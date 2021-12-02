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
python -m venv venv --upgrade-deps
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

- POST api/accounts/
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

## Update User Artist

- PUT api/accounts/1/
- Status HTTP 200 OK

```json
{
    "solo": true,
    "hour_price": 180.00
}
```
- Expected response

```json
{
    "id": 1,
    "username": "John",
    "email": "john@gmail.com",
    "is_superuser": false,
    "phone": "199898989",
    "solo": true,
    "hour_price": 180.00
}
```

- If you try to update a non-existent user
- Status HTTP 404 NOT FOUND

```json
{
    "error": "User not founded."
}
```

## Create User Owner

- POST api/accounts/
- Status HTTP 201 CREATED

```json
{
    "username": "Doe",
    "password": "67890",
    "email": "doe@gmail.com",
    "is_superuser": true
}
```
- Expected response

```json
{
    "id": 2,
    "username": "Doe",
    "email": "doe@gmail.com",
    "is_superuser": true
}
```

- If there is an attempt to create a username who is already registered.
- Status HTTP 409 CONFLICT.

```json
{
    "error": "User already exists!"
}
```

## Update User Owner

- PUT api/accounts/2/
- Status HTTP 200 OK

```json
{
    "username": "JDoe",
}
```
- Expected response

```json
{
    "id": 2,
    "username": "JDoe",
    "email": "doe@gmail.com",
    "is_superuser": true
}
```

- If you try to update a non-existent user
- Status HTTP 404 NOT FOUND

```json
{
    "error": "User not founded."
}
```

## Showing all Users

- GET api/accounts/
- Status HTTP 200 OK
- Expected response

```json
{
    "id": 1,
    "username": "John",
    "email": "john@gmail.com",
    "is_superuser": false,
    "phone": "199898989",
    "solo": false,
    "hour_price": 150.00
},
{
    "id": 2,
    "username": "JDoe",
    "email": "doe@gmail.com",
    "is_superuser": true
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
    "error": "Username or password it's missing"
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

- POST api/events/
- Status HTTP 201 CREATED
> The event lineup will be included soon. 

```json
{
    "date": "2021-12-10 19:00:00",
    "repeat_date": "None",
    "address": {
        "street": "W Pine St",
        "neighbourhood": "Downtown Orlando",
        "number": 37,
        "city": "Orlando",
        "state": "Florida",
    },
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
    "date": "2021-12-10 19:00:00",
    "repeat_date": "None",
    "address": {
        "street": "W Pine St",
        "neighbourhood": "Downtown Orlando",
        "number": 37,
        "city": "Orlando",
        "state": "Florida",
    },
    "owner": "Michael",
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

- PUT api/events/1/
- Status HTTP 200 OK

```json
{
    "lineup": [
        {
            "artist": 1,
            "performance_datetime": "2021-12-10 20:00:00"
        },
        {
            "artist": 3,
            "performance_datetime": "2021-12-10 21:00:00"
        }
    ]
}
```

- Expected response

```json
{
    "id": 1,
    "date": "2021-12-10 19:00:00",
    "repeat_date": "None",
    "address": {
        "street": "W Pine St",
        "neighbourhood": "Downtown Orlando",
        "number": 37,
        "city": "Orlando",
        "state": "Florida",
    },
    "owner": "Michael",
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
            "artist": "John",
            "performance_datetime": "2021-12-10 20:00:00"
        },
        {
            "artist": "LadyGaga",
            "performance_datetime": "2021-12-10 21:00:00"
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
    "error": "Invalid event id."
}
```

- If you try to pass a artist_id that doesn't exist
- Status HTTP 404 NOT FOUND

```json
{
    "error": "Invalid artist id."
}
```

## Cadidature Artist On Event

- PATCH api/events/1/candidatures/
- Status HTTP 200 OK

```json
// THE LOGGED ARTIST WILL BE PASSED
```

- Expected response

```json
{
    "msg": "Application made successfully"
}
```

## Owner Administration Candidatures

- PATCH api/events/1/candidatures/
- Status HTTP 200 OK

```json
{
    "remove_artists": [2, 3]
}
```

- Expected response

```json
{
    "address": {
        "street": "W Pine St",
        "neighbourhood": "Downtown Orlando",
        "number": 37,
        "city": "Orlando",
        "state": "Florida",
    },
    "music_styles": [
        {
            "name": "Rock"
        },
        {
            "name": "Country"
        }
    ],
    "lineup": [
        {
            "artist": "John",
            "performance_datetime": "2021-12-10 20:00:00"
        },
        {
            "artist": "LadyGaga",
            "performance_datetime": "2021-12-10 21:00:00"
        }
    ],
    "candidatures": [
        {
            "username": "Robert",
            "email": "robert@gmail.com",
            "phone": "999898989",
            "solo": false,
            "hour_price": 130
        },
        {
            "username": "Selena",
            "email": "selena@gmail.com",
            "phone": "999797979",
            "solo": false,
            "hour_price": 190
        }
    ]
}
```

## Showing all Events

- GET api/events/
- Status HTTP 200 OK

```json
{
    "id": 1,
    "date": "2021-12-10 19:00:00",
    "repeat_date": "None",
    "address": {
        "street": "W Pine St",
        "neighbourhood": "Downtown Orlando",
        "number": 37,
        "city": "Orlando",
        "state": "Florida",
    },
    "owner": "Elvis",
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
            "artist": "John",
            "performance_datetime": "2021-12-10 20:00:00"
        },
        {
            "artist": "LadyGaga",
            "performance_datetime": "2021-12-10 21:00:00"
        }
    ]
},
{
    "id": 2,
    "date": "2021-12-15 20:00:00",
    "repeat_date": "None",
    "address": {
        "street": "2nd Ave",
        "neighbourhood": "Rose Hill",
        "number": 519,
        "city": "New York",
        "state": "New York",
    },
    "owner": "Michael",
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
            "artist": "John",
            "performance_datetime": "2021-12-15 21:00:00"
        },
        {
            "artist": "LadyGaga",
            "performance_datetime": "2021-12-15 22:00:00"
        },
        {
            "artist": "Richard",
            "performance_datetime": "2021-12-15 23:00:00"
        }
    ]
}
```

## Delete Event

- DELETE api/events/1/
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

## Create Feedback

- POST api/feedbacks/
- Status HTTP 201 CREATED

```json
{
    "from_user": 1,
    "description": "Some feedback description",
    "stars": 3,
    "event": 1,
    "addressed_user": 2
}
```

- Expected response

```json
{
    "id": 1,
    "from_user": "Doe",
    "description": "Some feedback description",
    "stars": 3,
    "event": {
        "date": "2021-12-10 19:00:00",
        "repeat_date": "None",
        "address": {
            "street": "W Pine St",
            "neighbourhood": "Downtown Orlando",
            "number": 37,
            "city": "Orlando",
            "state": "Florida",
        },
        "owner": "Doe",
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
                "artist": "John",
                "performance_datetime": "2021-12-10 20:00:00"
            },
            {
                "artist": "LadyGaga",
                "performance_datetime": "2021-12-10 21:00:00"
            }
        ]
    },
    "addressed_user": "John"
}
```