import os
import sys
from flask import Flask, request, abort, jsonify,send_from_directory, safe_join
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
UPLOAD_DIRECTORY = 'images\\'
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response
    
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=["GET"])
  def get_categories():
    cats = Category.query.all()
    cats = [cat.format() for cat in cats]
    return jsonify(categories=cats)
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    page = request.args.get('page',1, type=int)
    all_questions = Question.query.all()
    total_questions = len(all_questions)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = all_questions[start:end]
    questions = [q.format() for q in questions]
    categories = Category.query.all()
    categories = [cat.format() for cat in categories]
    current_category=1
    return jsonify(
      questions=questions, 
      total_questions=total_questions,
      categories=categories,
      current_category=current_category
      )
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=["DELETE"])
  def delete_question(id):
    question = Question.query.get(id)
    if not question:
      abort(404)
    question.delete()
    return jsonify(),204
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions',methods=["POST"])
  def add_question():
    try:
      data = request.get_json()
      new_question = Question(**data)
      new_question.insert()
    except:
      print(sys.exc_info())
      abort(400)
    return jsonify(),201
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  # NOTE: fix the pagination problem
  @app.route('/questions/search',methods=["POST"])
  def search_questions():
    data = request.get_json()
    search_term = f"%{data['searchTerm']}%"
    total_questions = Question.query.filter(Question.question.ilike(search_term)).all()
    page = request.args.get('page',1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    
    categories = Category.query.all()
    categories = [cat.format() for cat in categories]
    found_questions = total_questions[start:end]
    found_questions = [ fq.format() for fq in found_questions]
    return jsonify(questions = found_questions,total_questions = len(total_questions), current_category=0,categories=categories)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route("/categories/<int:id>/questions", methods=["GET"])
  def get_questions_by_category(id):
      category = Category.query.get(id)
      if not category:
          abort(404) 
      questions = Question.query.filter_by(category=id).all()
      total_questions = len(questions)

      page = request.args.get('page',1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      questions = questions[start:end]
      questions = [q.format() for q in questions]
      categories = Category.query.all()
      categories = [cat.format() for cat in categories]
      return jsonify(
      questions=questions, 
      total_questions=total_questions,
      current_category=id,
      categories=categories
      )  
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=["POST"])
  def get_quiz_question():
    data = request.get_json()
    cat = int(data['quiz_category'])
    pre_questions = data['previous_questions']
    all_questions = Question.query.filter(Question.category==cat).filter(Question.id.notin_(pre_questions)).all()
    if len(all_questions):
      question = random.choice(all_questions)
    else:
      question=None

    return jsonify(question = question.format())
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def error_not_found(error):
      return jsonify(
          {
              'success':False,
              'message':"resource not found"
          }
      ),404

  @app.errorhandler(400)
  def error_bad_request(error):
      return jsonify(
          {
              'success':False,
              'message':"bad request"
          }
      ),400

  @app.errorhandler(422)
  def error_not_found(error):
      return jsonify(
          {
              'success':False,
              'message':"unprocessable"
          }
      ),422
  @app.errorhandler(500)
  def error_internal(error):
      return jsonify(
          {
              'success':False,
              'message':"Internal Error has happended"
          }
      ),500
  @app.route('/images/<path:filename>')
  def serve_image(filename):   
    return app.send_static_file(filename)

  return app

    