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

  CORS(app)

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response
    
  @app.route('/categories', methods=["GET"])
  def get_categories():
    cats = Category.query.all()
    cats = [cat.format() for cat in cats]
    return jsonify(categories=cats)

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

  @app.route('/questions/<int:id>', methods=["DELETE"])
  def delete_question(id):
    question = Question.query.get(id)
    if not question:
      abort(404)
    question.delete()
    return jsonify(),204

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


  @app.route('/questions/search',methods=["POST"])
  def search_questions():
    data = request.get_json()
    if not data.get('searchTerm'):
      abort(422)
    search_term = f"%{data.get('searchTerm')}%"
    total_questions = Question.query.filter(Question.question.ilike(search_term)).all()
    page = request.args.get('page',1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    
    categories = Category.query.all()
    categories = [cat.format() for cat in categories]
    found_questions = total_questions[start:end]
    found_questions = [ fq.format() for fq in found_questions]
    return jsonify(questions = found_questions,total_questions = len(total_questions), current_category=0,categories=categories)


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
 

  @app.route('/quizzes', methods=["POST"])
  def get_quiz_question():
    data = request.get_json()
    if not data:
      abort(422)
    if not data.get('quiz_category'):
      abort(422)
    cat = int(data.get('quiz_category'))
    pre_questions = data.get('previous_questions',[])
    all_questions = Question.query.filter(Question.category==cat).filter(Question.id.notin_(pre_questions)).all()
    if len(all_questions):
      question = random.choice(all_questions)
    else:
      question=None

    return jsonify(question = question.format())
 
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
  return app

    