import unittest
from registration_payment_service import app, users, payments


class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
#Clears users and payments prior to testing
    def setUp(self):
        users.clear()
        payments.clear()
#Successful user registration
    def test_register_user_success(self):
        response = self.client.post('/users', json={
            "username": "anya123",
            "password": "Password1",
            "email": "804anya@gmail.com",
            "dob": "2004-04-08",
            "credit_card": "1234567890123456"
        })
        self.assertEqual(response.status_code, 201)
#Unsuccessful user registration: underage
    def test_register_user_underage(self):
        response = self.client.post('/users', json={
            "username": "anya123",
            "password": "Password1",
            "email": "804anya@gmail.com",
            "dob": "2010-01-01"
        })
        self.assertEqual(response.status_code, 403)
#Unsuccessful user registration: username already exists
    def test_register_user_username_exists(self):
        self.client.post('/users', json={
            "username": "anya123",
            "password": "Password1",
            "email": "804anya@gmail.com",
            "dob": "2004-04-08"
        })
        response = self.client.post('/users', json={
            "username": "anya123",
            "password": "Password1",
            "email": "804anya@gmail.com",
            "dob": "2004-04-08"
        })
        self.assertEqual(response.status_code, 409)
#Successful payment 
    def test_process_payment_success(self):
        self.client.post('/users', json={
            "username": "anya123",
            "password": "Password1",
            "email": "804anya@gmail.com",
            "dob": "2004-04-08",
            "credit_card": "1234567890123456"
        })
        response = self.client.post('/payments', json={
            "credit_card": "1234567890123456",
            "amount": 100
        })
        self.assertEqual(response.status_code, 201)
#Unsuccessful payment: Invalid Credit card no.
    def test_process_payment_invalid_credit_card(self):
        response = self.client.post('/payments', json={
            "credit_card": "0000000000000000",
            "amount": 100
        })
        self.assertEqual(response.status_code, 404)
#Successful user filtering: Credit card = Yes
    def test_get_users_with_credit_card_filter(self):
        self.client.post('/users', json={
            "username": "anya123",
            "password": "Password1",
            "email": "804anya@gmail.com",
            "dob": "2004-04-08",
            "credit_card": "1234567890123456"
        })
        response = self.client.get('/users?CreditCard=Yes')
        self.assertEqual(response.status_code, 200)
        self.assertIn('1234567890123456', str(response.data))
#Successful user filtering: Credit card = No
    def test_get_users_without_credit_card_filter(self):
        self.client.post('/users', json={
            "username": "anya111",
            "password": "Password1",
            "email": "804anya@gmail.com",
            "dob": "2004-04-08"
        })
        response = self.client.get('/users?CreditCard=No')
        self.assertEqual(response.status_code, 200)
        self.assertIn('anya111', str(response.data))


if __name__ == "__main__":
    unittest.main()
