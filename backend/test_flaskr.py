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
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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

    def test_get_paginated_questions(self):
        """tests success of pagination"""
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_request_beyond_valid_page(self):
        """tests error for trying to access unavailable page"""
        res = self.client().get('/questions?page=10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_categories(self):
        """test to check categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_request_non_existing_category(self):
        """test error for non existing category"""
        res = self.client().get('/categories/10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions(self):
        """test to check questions"""
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_question(self):
        """test to check deleting questions"""
        res = self.client().delete('/question/5')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_sent_delete_non_existing_question(self):
        """test error for non existing question"""
        res = self.client().delete('/question/z')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_submit_question(self):
        """tests suscessful submission"""
        new_question = {
            'question': 'new_question',
            'answer': 'new_answer',
            'difficulty': 'new_difficulty',
            'category': 'new_category'
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_add_question(self):
        """test error for non existing question"""
        new_question = {
            'question': 'new_question',
            'answer': 'new_answer',
            'difficulty': 'new_difficulty',
            'category': 'new_category'
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_search_question(self):
        """test  question search"""
        res = self.client().post('/questions', json={'search_term': ''})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_search_question(self):
        """test  question search"""
        res = self.client().post('/questions', json={'search_term': ''})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_by_category(self):
        """test category listing"""
        res = self.client().get('/category/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_questions_by_category(self):
        """test category listing"""
        res = self.client().get('/category/z/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_available_question(self):
        """test quiz questions"""
        res = self.client().post('/quiz/question',
                                 json={'category': 0, 'previous_questions': []})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['data'])
        res = self.client().get('/quiz/question')
        self.assertEqual(res.status_code, 405)

    def test_available_question(self):
        """test quiz questions"""
        data = json.loads(res.data)
        res = self.client().post('/quiz/question',
                                 json={'category': 0, 'previous_questions': []})
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
