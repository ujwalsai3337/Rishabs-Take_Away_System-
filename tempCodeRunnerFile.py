from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import csv
import os
import random
import string
from send_email import send_email
from datastructure import *
from flask_mail import Mail, Message
from random import randint

app = Flask(__name__, static_url_path='/static')

c = CustomerQueue()

app.secret_key = os.urandom(24)  # Generate a secret key

phone = 0

randomNumber = 0

# Route for the sign-up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global randomNumber
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Generate a 6-digit OTP
        otp = ''.join(random.choices(string.digits, k=6))

        # Write the user data and OTP to the CSV file
        with open('users.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([first_name, last_name, email, username, password, otp])

        # Send the OTP to the user's email
        randomNumber = randint(100000, 999999)

        send_email(email, "OTP", f"Here is your otp for verification : {randomNumber}")

        return redirect(url_for('verify_otp', email=email))

    return render_template('signin.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    global randomNumber
    if request.method == 'POST':
        entered_otp = request.form.get('verify-otp')
        # Read the user data from the CSV file
        if str(entered_otp) == str(randomNumber):
            return render_template('lunch.html', error=False)
        
    email = request.args.get('email')

    return render_template('lunch.html', error=False, email=email)



# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    global phone
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone = username
        # Read the user data from the CSV file
        with open('users.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) >= 5 and row[3] == username and row[4] == password:
                    # Store the phone number in the session variable
                    session['phone'] = row[2]
                    return redirect(url_for('dashboard'))
        
        return render_template('login.html', error=True)
    
    return render_template('login.html', error=False)


# Route for the dashboard page
@app.route('/dashboard')
def dashboard():
    return render_template('lunch.html')


@app.route('/submit_order', methods=['POST'])
def submit_order():
    global c
    global phone
    items = request.form.getlist('item')
    quantities = request.form.getlist('quantity')
    price = request.form.getlist('price')

    print(items, quantities, price)

    if len(items) != len(quantities):
        return 'Invalid order data', 400


    c.enqueue_customer(phone)

    with open('cart.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item, quantity, p in zip(items, quantities, price):
            c.add_order(phone, item, quantity, p)
            writer.writerow([item, quantity, phone, int(p)*int(quantity)])
    
    
    response = {'message': 'Order submitted successfully'}
    c.display_customers()
    return jsonify(response), 200

@app.route("/manager", methods=["GET"])

def manager():
    global c
    customers = []
    cur = c.head
    while cur:
        customer = {
            'customer_id': cur.customer_id,
            'orders': []
        }
        order_cur = cur.order_head
        while order_cur:
            order = {
                'item_name': order_cur.item_name,
                'quantity' : order_cur.quantity,
                'price': int(order_cur.price)*int(order_cur.quantity)
            }
            customer['orders'].append(order)
            order_cur = order_cur.next
        customers.append(customer)
        cur = cur.next
    print(customers)
    return render_template("manager.html", customers=customers)


if __name__ == '__main__':
    app.run(debug=True)
