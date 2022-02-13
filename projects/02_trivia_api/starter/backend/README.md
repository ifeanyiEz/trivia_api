# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with two keys: 
    success, with a value of "True", to show the status of the response; and
    categories, that contains a object of id: category_string key:value pairs. 
    Example:
    {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
    }


GET '/api/v1.0/questions?page=${integer}'
- Fetches a dictionary of questions in paginated format, the total nmuber of questions, all categories and also indicates the response status.
- Request Arguments: Page of type: integer
- Returns: An object with questions organized in pages of 10 questions maximum, total questions in 
  the DB, all the categories as well as response status.
  Example:
    {
        "success": true,
        "questions": [
            {
                "id": 29, 
                "question": "What is the best online learning platform in the world?",
                "answer": "Udacity", 
                "difficulty": 5,
                "category": 4 
            },

        ],
        "total_questions": 33,
        "categories": {
            '1' : "Science",
            '2' : "Art",
            '3' : "Geography",
            '4' : "History",
            '5' : "Entertainment",
            '6' : "Sports"
        }
    }


GET '/api/v1.0/categories/${id}/questions'
- Fetches a dictionary of questions for a given category in paginated format, the given category and the total number of questions in that category. The response status is also included.
- Request Arguments: Page: type, integer
- Returns: An object with questions organized in pages of 10 questions maximum, the total 
  number of questions in the given category, and the given category. Including the response status. 
  Example:
  {
      "success": true,
      "questions": [
          {
            "id": 29, 
            "question": "What is the best online learning platform in the world?",
            "answer": "Udacity", 
            "difficulty": 5,
            "category": 4
          },

      ],
      "total_questions": 12,
      "current_category": "History"
  }


DELETE '/api/v1.0/questions/${id}'
- Deletes a given question using the id of the question
- Request Arguments: question id - type, integer
- Returns: An object containing the response status, the deleted question id, and the total number of questions remaining in the database. 
  Example:
  {
      "success": true,
      "deleted": 'question_id = 29',
      "total_questions": 32
  }


POST '/api/v1.0/questions'
- This sends a post request which adds a new question to the database.
- Request Body: An object containing the actual question, the accompanying answer, the question's category id, and the associated difficulty level. 
  Example:
  {
      "question": "What is the best online learning platform in the world?",
      "answer": "Udacity",
      "category": 4,
      "difficulty": 5
  }
- Returns: An object containing the response status, the id of the newly added question, and the new total number of questions in the database.
  Example:
  {
      "success":  true,
      "created": 'question_id = 29',
      "total_questions": 33
  }


POST '/api/v1.0/questions/search'
- This sends a post request to search the database for a question or questions that match the search criterion. In this case, search criterion is a search term.
- Request Body: An object containing the word or words the user is looking for, the search term. 
  Example:
  {
      "searchTerm": 'palace'
  }
- Returns: An object containing the response status, a list of formated questions which contain the search term and are organized into pages of 10 questions maximum, then the total number of questions that match the search criterion.
  Example:
   {
      "success": true,
      "questions": [
            {
                "answer": "The Palace of Versailles", 
                "category": 3, 
                "difficulty": 3, 
                "id": 14, 
                "question": "In which royal palace would you find the Hall of Mirrors?"
            },

        ],
      "total_questions": 1
  }

POST '/api/v1.0/quizzes'
- This sends a post request to the database so as to fetch the questions one at a time in order to play the quiz.
- Request Body: This is an object containing a list of the ids of previously attempted questions, and the chosen category which is itself an object containing the category type and id.
  Example:
  {
    "previous_questions": [13], 
    "quiz_category": {
        "type": 'Geography', 
        "id": '3'
        }
  }
- Returns: An object which contains a single formated random question from the chosen category and the response status. 
  Example:
  {
    "success": true
    "question": {
        "answer": "Nunavut", 
        "category": 3, 
        "difficulty": 4, 
        "id": 37, 
        "question": "What is the largest province in Canada by land mass"
        }
  }
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
