import unittest
from unittest import TestCase

from fastapi.testclient import TestClient

from app import app


class AppTestCase(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Server running!')

    def test_resize(self):
        response = self.client.get('/resize')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Resized')


if __name__ == '__main__':
    unittest.main()
