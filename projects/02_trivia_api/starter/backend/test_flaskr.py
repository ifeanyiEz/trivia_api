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
            'question': 'Can I add a quesion without an answer?',
            'answer': 'No, you cannot',
            'category': '1',
            'difficulty': '2'
        }

        self.new_question1 = {
            'question': 'Can I add a quesion without an answer?',
            'answer': '',
            'category': '1',
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
    DONE
    Write at least one test for each test for successful operation and for expected errors.
    """

#__________________DEFINE OPERATIONAL TESTS_________________#

    #____________________Add Complete Question_______________#

    def test_add_complete_question(self):
        '''Checking to see if questions are added as expected'''
        resp = self.client().post("/questions", json = self.new_question)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue((data['total_questions']))
    
    #_________________Add Incomplete Question________________#

    def test_add_incomplete_question(self):
        '''Checking to see if incomplete questions are rejected as expected'''
        resp = self.client().post("/questions", json=self.new_question1)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    #_________________List Questions________________#

    def test_list_questions(self):
        '''Checking to see if questions are listed as expected'''
        resp = self.client().get("/questions")
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['categories']), 6)


    #____________________List Categories_________________#

    def test_list_categories(self):
        '''Checking to ensure that quiz categories are listed as expected'''
        resp = self.client().get("/categories")
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)


    #______________List Questions By Category______________#

    def test_list_questions_by_category(self):
        '''Checking to ensure that listing questions by category works as expected'''
        resp = self.client().get("/categories/4/questions")
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertEqual(data['current_category'], "History")


    #_______________Delete Question By ID________________#

    def test_delete_question_by_id(self):
        '''Checking to ensure that questions are deleted by question_id'''
        resp = self.client().delete("/questions/66")
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(data['deleted'], "question_id = 66")
        self.assertTrue(data['total_questions'])


    #_______________Play Quiz_____________________#

    def test_play_quiz(self):
        '''Checking to ensure that the quiz plays as expected'''
        resp = self.client().post("/quizzes", json = {
            'previous_questions': [13], 'quiz_category': {'type': 'Geography', 'id': '3'}
        })
        data = json.loads(resp.data)
        quiz = Question.query.filter(Question.category == 3).all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)


    #_______________Play Quiz: Wrong Data________________#

    def test_play_quiz_wrong_data(self):
        '''Checking quiz response with the wrong quiz data'''
        resp = self.client().post("/quizzes", json = {
            'previous_questions': [50], 'quiz_category': {'type': 'Geography', 'id': '21'}
        })
        data = json.loads(resp.data)
        quiz = Question.query.filter(Question.category == 21).all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], False)


    #_______________Successful Search: Question Found____________#

    def test_successful_search_found_question(self):
        '''Checking for successful question search with results'''
        resp = self.client().post("/questions/search", json = {'searchTerm': "palace"})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])


    #______________Successful Search: Question Not Found___________#

    def test_successful_search_question_not_found(self):
        '''Checking for successful question search without results'''
        resp = self.client().post("/questions/search", json = {'searchTerm': "palaces "})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

#_________________DEFINE EXPECTED ERROR TESTS_________________#

    #_____________Error 400 Handler______________#

    def test_add_incomplete_question(self):
        '''Checking to see if error 400 handler is working as expected'''
        resp = self.client().post("/questions", json=self.new_question1)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The server could not understand the request due to invalid syntax")


    #_____________Error 404 Handler______________#

    def test_list_questions_beyond_valid_page(self):
        '''Checking to see if error 404 handler works as expected'''
        resp = self.client().get("/questions?page=20")
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The server can not find the requested resource")


    #_____________Error 405 Handler______________#

    def test_not_allowed_method(self):
        '''Checking to see if error handler 405 is working as expected'''
        resp = self.client().get("/questions/2")
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "This method is not allowed for the requested URL")


    #_____________Error 422 Handler______________#

    def test_delete_nonexisting_question(self):
        '''Checking to see if error 422 handler works as expecrted'''
        resp = self.client().delete('/questions/59')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The request was unable to be followed due to semantic errors")



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()