import os
import tempfile
import unittest
from pathlib import Path

import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.database = tempfile.NamedTemporaryFile(delete=False)
        self.database.close()
        app.DATABASE = Path(self.database.name)
        app.init_db()
        self.client = app.app.test_client()

    def tearDown(self):
        os.unlink(self.database.name)

    def test_valid_message_is_saved(self):
        response = self.client.post('/api/messages', json={'name': 'Анна', 'email': 'anna@example.com', 'message': 'Цікавить курс B'})
        self.assertEqual(response.status_code, 201)
        with app.get_db() as connection:
            self.assertEqual(connection.execute('SELECT COUNT(*) FROM messages').fetchone()[0], 1)

    def test_invalid_message_is_rejected(self):
        response = self.client.post('/api/messages', json={'name': 'A', 'email': 'wrong', 'message': ''})
        self.assertEqual(response.status_code, 400)

    def test_messages_require_authentication(self):
        response = self.client.get('/api/messages')
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
