import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


#________________________REFERENCES:____________________________#

# https://flask.palletsprojects.com/en/2.0.x/api/ 
# https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/
# https://flask.palletsprojects.com/en/2.0.x/patterns/packages/
# https://flask.palletsprojects.com/en/2.0.x/testing/
# https://pynative.com/python-random-choice/
# https://www.techiedelight.com/generate-random-numbers-specified-range-python/  
# https://realpython.com/list-comprehension-python/
# https://tedboy.github.io/flask/generated/generated/flask.Request.get_json.html
# https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask
# https://linuxize.com/post/curl-command-examples/?linuxize-blog%5Bquery%5D=cu
# https://www.educative.io/edpresso/how-to-send-a-delete-request-with-curl
# https://betterprogramming.pub/simple-flask-pagination-example-4190b12c2e2e


QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.arg.get('page', 1, type = int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  

#______________________SET UP CORS AND CORS HEADERS__________________#

  '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,True")
    response.headers.add("Access-Control-Allow-Methods", "DELETE,GET,OPTIONS,PATCH,POST,PUT")
    return response


#____________________DEFINE ENDPOINTS____________________________#


  #______________Get all Categories____________#
  '''
  @DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories', methods=['GET'])
  def list_categories():

    #Get all the quiz categories from the DB and format them using the format() method
    quiz_categories = Category.query.order_by(Category.id).all()
    formatted_categories = [category.format() for category in quiz_categories]

    #If there are no categories, show a not-found (404) error
    if len(formatted_categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': {category.id: category.type for category in quiz_categories}
    })



  #_______________Get all Questions Paginated____________#
  '''
  @DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions', methods=['GET'])
  def list_questions():

    #Define the page parameter
    page = request.args.get('page', 1, type=int)

    quiz_categories = Category.query.order_by(Category.id).all()

    #Get all questions from the DB, order them by question_id and present only 10 questions maximum, per page
    questions = Question.query.order_by(Question.id).paginate(page = page, per_page = QUESTIONS_PER_PAGE)

    #If there are no questions in the DB, show a not-found (404) error
    if len(questions.items) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': [question.format() for question in questions.items],
      'total_questions': questions.total,
      'categories': {category.id: category.type for category in quiz_categories}
    })



  #_____________Delete Single Question by ID_________________#
  '''
  @DONE: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    try:

      #Get the question for deletion from the DB using the specified question_id
      question = Question.query.filter_by(id = question_id).one_or_none()

      #If it's not in the DB show a not-found error (404), else delete the question
      if question is None:
        abort(404)
      question.delete()

      #Let's know how many questions are left in the DB
      questions = Question.query.all()

      return jsonify({
        'success': True,
        'deleted': 'question_id = {}'.format(question.id),
        'total_questions': len(questions)
      })
    except:
      abort(422)


  #___________________Add a New Question____________________#
  '''
  @DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  def add_new_question():

    body = request.get_json()

    #Extract the question elements values from the request body
    question = body.get('question', None)
    answer = body.get('answer', None)
    category = body.get('category', None)
    difficulty = body.get('difficulty', None)

    try:
      error = False

      #Define the new question object and add it to the DB if all fields have valid values
      new_question = Question(question = question, answer = answer, category = category, difficulty = difficulty)

      if new_question.question == "" or \
        new_question.answer == "" or \
          new_question.category == "" or \
            new_question.difficulty == "":
            return jsonify({
              'success': False,
              'message': 'The server could not understand the request due to invalid syntax'
            }), 400
      else:
        new_question.insert()

      #Let's know how many questions are now in the DB
      questions = Question.query.all()

      return jsonify({
        'success': True,
        'created': 'question_id = {}'.format(new_question.id),
        'total_questions': len(questions)
      })
    except error:
      abort(422)




  #_______________Search for Question by Search Term____________#
  '''
  @DONE: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only questions that include that string within their question. 
  Try using the word "title" to start.
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_questions():

    #Define the page parameter
    page = request.args.get('page', 1, type=int)

    body = request.get_json()

    #Get the search term from the request body
    search_term = body.get('searchTerm', None)

    try:
      error = False

      #If there's a search term, remove all blank spaces before and after it, else abort(404)
      if search_term is not None:
        search_text = search_term.strip()
      else:
        abort(404)
      
      #Get search results from the DB and present them in pages of 10 questions maximum, each
      search_results = Question.query.filter(Question.question.ilike('%' + search_text + '%')).order_by(Question.id).paginate(page=page, per_page=QUESTIONS_PER_PAGE)

      return jsonify({
        'success': True,
        'questions': [question.format() for question in search_results.items],
        'total_questions': search_results.total
      })
    
    except error:
      abort(422)



  #________________List Questions by Category_____________________#
  '''
  @DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def questions_by_category(category_id):

    #Define the page parameter
    page = request.args.get('page', 1, type=int)

    try:

      #Filter out questions by category_id, order them by question_id and present only 10 questions, maximum, per page
      category_questions = Question.query.filter_by(category = category_id).order_by(Question.id).paginate(page = page, per_page = QUESTIONS_PER_PAGE)

      current_category = Category.query.filter_by(id = category_id).one_or_none()

      #If there are no questions in the category show a not-found (404) error.
      if len(category_questions.items) == 0 or current_category is None:
        abort(404)

      return jsonify({
        'success': True,
        'questions': [question.format() for question in category_questions.items],
        'total_questions': category_questions.total,
        'current_category': current_category.type
      })
      
    except:
      abort(422)


  #___________________Get Questions To Play Quiz______________________#
  '''
  @DONE: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def show_random_question():

    body = request.get_json()

    #Extract previous questions and the chozen quiz category from the request body
    prev_questions = body['previous_questions']
    quiz_category = body['quiz_category']['id']

    try:
      error = False

      #If the chosen category is "All", get all questions from the DB, else get only questions for the category
      if quiz_category == 0:
        questions = Question.query.all()
      else:
        questions = Question.query.filter(Question.category == quiz_category).all()

      #Put all the unattempted questions in a list called questions_set
      questions_set = [question.format() for question in questions if question.id not in prev_questions]

      #As long as there are still questions in the question set continue selecting random questions
      if len(questions_set) != 0:

        random_question = random.choice(questions_set)
        return jsonify({
          'success': True,
          'question': random_question
        })
      else:
        return jsonify({
          'success': False,
        })

    except error:
      abort(422)

#____________________End Endpoints_______________________#


#____________________HANDLING ERRORS_____________________#

  '''
  @DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "The server could not understand the request due to invalid syntax"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "The server can not find the requested resource"
    }), 404

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "This method is not allowed for the requested URL"
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "The request was unable to be followed due to semantic errors"
    }), 422

  @app.errorhandler(500)
  def internal_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "The server has encountered an internal error"
    })

  return app

    