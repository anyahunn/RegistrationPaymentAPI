import re
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

#In-memory storage for registered users and payments
users = []
payments = []

#Helper functions for validation
def is_valid_username(username):
    return bool(re.match(r"^[a-zA-Z0-9]+$", username))


def is_valid_password(password):
    return len(password) >= 8 and bool(re.search(r"[A-Z]", password)) and bool(re.search(r"\d", password))


def is_valid_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def is_valid_credit_card(card_number):
    return bool(re.match(r"^\d{16}$", card_number))


def calculate_age(dob):
    dob = datetime.strptime(dob, "%Y-%m-%d")
    age = (datetime.now() - dob).days // 365
    return age


#Registration Service
@app.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()

    #Validate fields
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    dob = data.get('dob')
    credit_card = data.get('credit_card')

    if not is_valid_username(username):
        return jsonify({"error": "Invalid username. It should be alphanumeric, no spaces."}), 400
    if not is_valid_password(password):
        return jsonify({"error": "Invalid password. It should be at least 8 characters long with one uppercase letter and one number."}), 400
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format."}), 400
    if not dob or calculate_age(dob) < 18:
        return jsonify({"error": "User must be 18 years or older."}), 403
    if credit_card and not is_valid_credit_card(credit_card):
        return jsonify({"error": "Invalid credit card number. It should have 16 digits."}), 400

    #Check if username already exists
    for user in users:
        if user['username'] == username:
            return jsonify({"error": "Username already exists."}), 409

    #Register user
    user = {
        "username": username,
        "password": password,
        "email": email,
        "dob": dob,
        "credit_card": credit_card
    }
    users.append(user)

    return jsonify({"message": "User registered successfully."}), 201


#Get all users with filter options
@app.route('/users', methods=['GET'])
def get_users():
    credit_card_filter = request.args.get('CreditCard')

    if credit_card_filter == "Yes":
        filtered_users = [user for user in users if user.get('credit_card')]
    elif credit_card_filter == "No":
        filtered_users = [user for user in users if not user.get('credit_card')]
    else:
        filtered_users = users

    return jsonify(filtered_users)

#Payment Service
@app.route('/payments', methods=['POST'])
def process_payment():
    data = request.get_json()

    credit_card = data.get('credit_card')
    amount = data.get('amount')

    if not is_valid_credit_card(credit_card):
        return jsonify({"error": "Invalid credit card number. It should have 16 digits."}), 400
    if not isinstance(amount, int) or not (0 < amount < 1000):
        return jsonify({"error": "Invalid amount. It should be a number between 1 and 999."}), 400

    #Check if credit card exists in registered users
    user = next((user for user in users if user['credit_card'] == credit_card), None)
    if not user:
        return jsonify({"error": "Credit card number not registered."}), 404

    #Register payment
    payment = {
        "credit_card": credit_card,
        "amount": amount
    }
    payments.append(payment)

    return jsonify({"message": "Payment processed successfully."}), 201


if __name__ == "__main__":
    app.run(debug=True)
