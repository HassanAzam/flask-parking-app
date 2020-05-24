import json
import os
import unittest
from test.support import EnvironmentVarGuard


def setup_test_data():

    from app.services.utils.scripts_util import ScriptUtility

    ScriptUtility.create_roles()
    ScriptUtility.create_admin("testadmin@mailinator.com", "testadmin")


class TestRegisterAPI(unittest.TestCase):

    def setUp(self):

        # Set up env variable APP_CONFIG_PATH
        # It contains the path of required external config file
        self.env = EnvironmentVarGuard()
        self.env.set("APP_CONFIG_PATH", "D:/HassanWorkSpace/flask-parking-app/parking_app_test_config.py")

        with self.env:
            from app import app, db
            self.app = app
            self.db = db

            # Initialize test environment database
            db.create_all()

            # Setup test data
            setup_test_data()

            self.test_app_client = app.test_client()

    def test_register_api_success(self):

        # Prepare test data for RegisterAPI
        request_data = {
            "email": "user1@mailinator.com",
            "password": "12345"
        }

        resp = None
        with self.test_app_client as c:
            resp = c.post("/user/register", json=request_data)
            print(resp.data)

        resp_json = json.loads(resp.data)

        self.assertEqual("Success", resp_json["message"])
        self.assertEqual(0, resp_json["status_code"])

    def test_register_api_with_already_registered_email(self):

        # Prepare test data for RegisterAPI
        request_data = {
            "email": "duplicate@mailinator.com",
            "password": "12345"
        }

        resp = None
        with self.test_app_client as c:
            r = c.post("/user/register", json=request_data)
            print(r.data)
            # Try to register again
            resp = c.post("/user/register", json=request_data)
            print(resp.data)

        resp_json = json.loads(resp.data)

        self.assertEqual("This email is already in use.", resp_json["message"])
        self.assertEqual(101, resp_json["status_code"])

    def tearDown(self):

        # Flush test db
        self.db.session.remove()
        self.db.drop_all()
