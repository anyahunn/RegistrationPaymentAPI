Flask Payment and User Registration Service
This is a simple Flask-based API service for registering users, validating their details, and processing payments. It supports user registration with basic validation, user information retrieval, and payment processing.

Features
User Registration: Allows users to register by providing a username, password, email, date of birth, and credit card information (optional).
User Listing: Fetches all users with optional filters (based on credit card availability).
Payment Processing: Allows users to make payments by providing a valid credit card and an amount (between 1 and 999).

Installation
Requirements
Python 3.x
Flask
Setup

Install Python dependencies:
pip install -r requirements.txt

Run the application:

python video_streaming_service.py
The API will be accessible at http://127.0.0.1:5000/.

API Endpoints
1. Register User
POST /users
Registers a new user.

Request Body Example:
json
{
    "username": "exampleUser123",
    "password": "Password1",
    "email": "example.user@example.com",
    "dob": "1990-05-01",
    "credit_card": "1234567890123456"
}

Validation Rules:
Username: Alphanumeric, no spaces.
Password: Minimum 8 characters with at least one uppercase letter and one number.
Email: Must be in a valid email format.
Date of Birth: User must be 18 years or older.
Credit Card: Should have 16 digits (optional).

Response:
201 Created: Successfully registered.
400 Bad Request: Invalid data.
409 Conflict: Username already exists.
403 Forbidden: User must be 18 or older.

2. Get Users
GET /users
Fetches all registered users with optional filters based on whether they have a credit card.

Query Parameters:
CreditCard (optional): Filter users based on credit card availability.
Yes: Show users with credit cards.
No: Show users without credit cards.
Response:
200 OK: Returns a list of users.

3. Process Payment
POST /payments
Processes a payment for a registered user.

Request Body Example:
json
{
    "credit_card": "1234567890123456",
    "amount": 100
}

Validation Rules:
Credit Card: Must be a 16-digit number.
Amount: Must be between 1 and 999 (inclusive).

Response:
201 Created: Payment processed successfully.
400 Bad Request: Invalid credit card or amount.
404 Not Found: Credit card not registered.
Helper Functions
is_valid_username(username): Validates the username (alphanumeric, no spaces).
is_valid_password(password): Validates the password (at least 8 characters, one uppercase letter, and one digit).
is_valid_email(email): Validates the email format.
is_valid_credit_card(card_number): Validates the credit card (16 digits).
calculate_age(dob): Calculates the age based on the date of birth.

Example Usage
Register a new user:
curl -X POST http://127.0.0.1:5000/users -H "Content-Type: application/json" -d "{\"username\": \"johnDoe123\", \"password\": \"Password1\", \"email\": \"john.doe@example.com\", \"dob\": \"2000-01-01\", \"credit_card\": \"9876543210987654\"}"

Get all users:
curl http://127.0.0.1:5000/users

Process a payment:
curl -X POST http://127.0.0.1:5000/payments -H "Content-Type: application/json" -d "{\"credit_card\": \"9876543210987654\", \"amount\": 50}"

4. Unit Tests
To run:
python -m unittest test.py

Response:
On Success: b.......
----------------------------------------------------------------------
Ran 7 tests in 0.019s

OK
