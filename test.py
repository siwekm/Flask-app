import unittest
from base64 import b64encode

import app
import os

class MyTestCase(unittest.TestCase):
    def test_pipeline(self):
        tester = app.app.test_client(self)

        auth = os.environ['BASIC_AUTH_USERNAME'] + ":" + os.environ['BASIC_AUTH_PASSWORD']
        auth = b64encode(bytes(auth, "utf-8"))
        # Test authentication
        headers = {
            'Authorization': 'Basic ' + auth.decode()
        }
        res = tester.get('/export', headers=headers)
        self.assertEqual(res.status_code, 200)

        # Test POST
        form = {"annotation": 12040765, "queue": 170679}
        res = tester.post('/export', data=form, headers=headers)
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()
