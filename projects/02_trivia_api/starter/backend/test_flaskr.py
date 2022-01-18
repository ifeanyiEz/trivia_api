import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("ezugworie", "E2u8w0r1e", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Why did the pidgeon cross the road?',
            'answer': 'To get to the other side',
            'category': '5',
            'difficulty': '2'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_add_question(self):
        '''Testing to see if questions are added as expected'''
        resp = self.client().post("/questions", json = self.new_question)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue((data['total_questions']))

    def test_list_questions(self):
        '''Testing to see if questions are listed as expected'''
        resp = self.client().get("/questions")
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['categories']), 6)

    def test_list_categories(self):
        '''Testing to ensure that quiz categories are listed as expected'''
        resp = self.client().get("/categories")
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)

    def test_delete_question(self):
        '''Testing to ensure that questions are deleted by question_id'''
        resp = self.client().delete("/questions/55")
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(data['deleted'], "question_id = 55")
        self.assertTrue(data['total_questions'])

    def test_play_quiz(self):
        '''Testing to ensure that the quiz plays as expected'''
        resp = self.client().post("/quizzes", json = {
            'previous_questions': [13], 'quiz_category': {'type': 'Geography', 'id': '3'}
        })
        data = json.loads(resp.data)
        quiz = Question.query.filter(Question.category == 3).all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_play_quiz_wrong_data(self):
        '''Checking quiz response with the wrong quiz data'''
        resp = self.client().post("/quizzes", json = {
            'previous_questions': [50], 'quiz_category': {'type': 'Geography', 'id': '21'}
        })
        data = json.loads(resp.data)
        quiz = Question.query.filter(Question.category == 21).all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], False)

    def test_successful_search_found_question(self):
        '''Checking for successful question search with results'''
        resp = self.client().post("/questions/search", json = {'searchTerm': "palace"})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])


    def test_successful_search_question_not_found(self):
        '''Checking for successful question search without results'''
        resp = self.client().post("/questions/search", json = {'searchTerm': "palaces "})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()