import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category,db

database_name = "trivia_test"
database_path = 'postgresql://postgres:123456@localhost:5432/{}'.format(database_name)


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = database_name        
        self.database_path = database_path
        setup_db(self.app, self.database_path)
        
        self.categories = [
            {
                'type': 'sports'
            }
        ]
        self.questions = [
            {
                'question': 'how old is messi?',
                'answer': '30',
                'category': 1,
                'difficulty': 3
            }
        ]
        # binds the app to the current context
        with self.app.app_context():
            # self.db = SQLAlchemy()
            self.db = db
            self.db.init_app(self.app)
            # clean the database beforehand
            self.db.drop_all()
            self.db.session.commit()
            
            # create all tables
            self.db.create_all()
            self.db.session.commit()

        with self.app.app_context():
            #insert the categories
            for category in self.categories:
                cat = Category(**category)
                self.db.session.add(cat)
                self.db.session.commit()

            for question in self.questions:
                ques = Question(**question)
                self.db.session.add(ques)
                self.db.session.commit()

    def tearDown(self):
        """Executed after reach test"""
        pass

    #testing the categories
    def test_get_categories_ok(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    #testing the categories 400 unexpected arguments
    def test_get_categories_400(self):
        res = self.client().get('/categories?zx=34')
        self.assertEqual(res.status_code, 400)

    #testing the questions
    def test_get_questions_ok(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])

    #testing the questions unexpected argument fails
    def test_get_questions_400(self):
        res = self.client().get('/questions?error=df')
        self.assertEqual(res.status_code, 400)
    
    #testing delete one questions ok
    def test_delete_one_question_ok(self):
        res = self.client().delete('/questions/1')
        self.assertEqual(res.status_code, 204)

    #testing delete one questions not found
    def test_delete_one_question_404(self):
        res = self.client().delete('/questions/101')
        self.assertEqual(res.status_code, 404)

    def test_add_one_question_ok(self):
        res = self.client().post('/questions',json={
            'question': 'how old is the pyramids in years?',
            'answer': '4000',
            'category': '1',
            'difficulty': '2'
        })

        self.assertEqual(res.status_code, 201)
        
    def test_add_one_question_400(self):
        res = self.client().post('/questions',json={
            'question': 'how old is the pyramids in years?',
            'answer': '4000',
            'category': '1',
            'difficulty': '2',
            'anything': True
        })

        self.assertEqual(res.status_code, 400)

    def test_search_questions_ok(self):
        res = self.client().post('/questions/search',json={
            'searchTerm': 'how'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['total_questions'],1)

    def test_search_questions_422(self):
        res = self.client().post('/questions/search',json={
            'searchTerm_fail': 'how'
        })
        self.assertEqual(res.status_code,422)

    def test_get_questions_by_category_ok(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(data['total_questions'],1)
        self.assertEqual(res.status_code,200)

    def test_get_questions_by_category_404(self):
        res = self.client().get('/categories/100/questions')
        self.assertEqual(res.status_code,404)
    def test_get_quiz_question_ok(self):
        res = self.client().post('/quizzes',json={
            'quiz_category': 1,
            'previous_questions': []
        })

        data = json.loads(res.data)

        self.assertTrue(data['question'])
        self.assertEqual(res.status_code, 200)

    def test_get_quiz_question_422(self):
        res = self.client().post('/quizzes')
        self.assertEqual(res.status_code, 422)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()