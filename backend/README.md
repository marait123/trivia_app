# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we"ll use handle the lightweight sqlite database. You"ll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we"ll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia { trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

Endpoints
- GET "/categories"
- GET "/questions"
- DELETE "/questions/{id}"
- POST "/questions"
- POST "/questions/search"
- GET "/categories/{id}/questions"
- POST "/quizzes"

GET "/categories"
- Fetches an array of category objects with {id,type} properties from the database
- Request Arguments: None
- Query Arguments: None
- Request Body: None
- Returns: an object with a categories property equal to array of category objects with {id,type} properties
- Example Response:
```json
   { 
    "categories":[
        {
            "id":1,
            "type":"history"
        },
        {            
            "id":2,
            "type":"sports"
        }
    ]
   }
```
-status: 200

GET "/questions"
- Fetches an array of question objects with {id,question,answer,category,difficulty} properties
- Request Arguments: None
- Query Arguments: 
    -page = the page number
- Request Body: None
- Returns: an object containing {questions, categories, total_questions, current_category} properties
- Example Response:
```json
    {
        "questions":[
            {
                "id":1,
                "question":"who?",
                "answer":"me",
                "category":1,
                "difficulty":1,
                "type":"history"
            }
        ], 
        "categories":[
            {
                "id":1,
                "type":"history"
            }
        ],
        "total_questions":1,
        "current_category":1
    }
```
- status:200


DELETE "/questions/id"
- Deletes an question from the database with id = id
- Request Arguments:
    -id -} the id of the question
- Query Arguments: None
- Request Body: None
- Returns: Nothing
-status 204

POST "/questions"
- Adds a question to the database
- Request Arguments:None
- Query Arguments: None
- Request Body: 
    - id : question id
    - question: the question string
    - answer: the answer to the question
    - difficulty: the difficulty of the question
- Returns: Nothing
-status 201

POST "/questions/search"
- Adds a question to the database
- Request Arguments:None
- Query Arguments: None
- Request Body: 
    - searchTerm : part of the question string to look for
- Returns: an object with {questions, total_questions,current_category,categories} properties
- Example Response
```json
{
    "categories": [
        {
            "id": 1,
            "type": "history"
        }
    ],
    "current_category": 1,
    "questions": [
        {
            "answer": "abu_dahb",
            "category": 1,
            "difficulty": 3,
            "id": 5,
            "question": "who killed ali the great of egypt?",
            "type": "history"
        }
    ],
    "total_questions": 1
}
```
- status 200


GET "/categories/{id}/questions"
- Fetches questions from the database the belong to category with id={id}
- Request Arguments:
    - {id} = the id of the category the questions belong to    
- Query Arguments:
    -page = the page number
- Request Body:
- Returns: an object with {questions, total_questions,current_category,categories} properties
- Example Response
```json
{
    "categories": [
        {
            "id": 1,
            "type": "history"
        }
    ],
    "current_category": 1,
    "questions": [
        {
            "answer": "abu_dahb",
            "category": 1,
            "difficulty": 3,
            "id": 5,
            "question": "who killed ali the great of egypt?",
            "type": "history"
        }
    ],
    "total_questions": 1
}
```
- status 200

POST "/quizzes"
- Fetches a random question from the database that doesn"t belong in the array of previous questions
- Request Arguments:None 
- Query Arguments: None
- Request Body:
    - quize_category = the category of the question
    - previous_questions = the array of the questions to be excluded when selecting the random quesion
- Returns: an object with {question} property
- Example Response
```json
{  
    "question":{
            "answer": "abu_dahb",
            "category": 1,
            "difficulty": 3,
            "id": 5,
            "question": "who killed ali the great of egypt?",
            "type": "history"
            }
}
```
- status 200




## Testing
To run the tests, run.  
***NOTE: mock data is supplied in test_flaskr.py  [you need not supply it]***
```
dropdb trivia_test
createdb trivia_test
python test_flaskr.py
```
