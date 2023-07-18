from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import csv
import os
import random
import string
from send_email import send_email
from datastructure import *
from random import randint
import threading
import time

app = Flask(__name__, static_url_path='/static')
app.debug = False

c = CustomerQueue()
food_production_department = FoodProductionDepartment()
lock = threading.Lock()

app.secret_key = os.urandom(24)  # Generate a secret key

emailg = ''

phone = 0

randomNumber = randint(100000, 999999)

food_items = []

customers = []

import sys

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug server')
    func()


# Function to reload the food production department every 5 seconds
def reload_food_production_department():
    global food_production_department
    while True:
        with lock:
            food_production_department = FoodProductionDepartment()
            current_customer = c.head
            while current_customer:
                current_order = current_customer.order_head
                while current_order:
                    food_production_department.enqueue_customer_order(
                        current_customer.customer_id,
                        current_order.item_name,
                        current_order.quantity,
                        current_customer.verification
                    )
                    current_order = current_order.next
                current_customer = current_customer.next
        time.sleep(5)

# Start a separate thread to reload the food production department
reload_thread = threading.Thread(target=reload_food_production_department)
reload_thread.start()

# Route for the sign-up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
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

        return render_template('verify_otp.html')

    return render_template('signin.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    global randomNumber
    if request.method == 'POST':
        entered_otp = request.form.get('verify-otp')
        # Read the user data from the CSV file
        print(str(entered_otp), str(randomNumber))
        if str(entered_otp) == str(randomNumber):
            return render_template('login.html', error=False)
        
    email = request.args.get('email')

    return render_template('signin.html')



# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    global phone
    global emailg
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
                    emailg = row[2]
                    session['phone'] = row[2]
                    return redirect(url_for('dashboard'))
        
        return render_template('login.html', error=True)
    
    return render_template('login.html', error=False)


# Route for the dashboard page
@app.route('/dashboard')
def dashboard():
    return render_template('lunch.html')

@app.route('/aboutpage')
def about():
    return render_template('aboutpage.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/home')
def home():
    return render_template('home.html')


   

@app.route('/submit_order', methods=['POST'])
def submit_order():
    global emailg
    global c
    global phone
    global randomNumber
    global food_items
    items = request.form.getlist('item')
    quantities = request.form.getlist('quantity')
    price = request.form.getlist('price')
    option = request.form.get('option')  # Get the selected option value
    payment = request.form.get('payment') 

    if len(items) != len(quantities):
        return 'Invalid order data', 400
    randomNumber = randint(100000, 999999)

    c.enqueue_customer(phone, option=option, payment=payment, verification=randomNumber)

    with open('cart.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item, quantity, p in zip(items, quantities, price):
            c.add_order(phone, item, quantity, p)
            writer.writerow([item, quantity, phone, int(p)*int(quantity)])
            
    # Update food_items inside the lock
    with lock:
        food_items = food_production_department.get_food_items()
    print("I'm here")

    response = {'message': 'Order submitted successfully'}
    return jsonify(response)


@app.route("/update_food_item_quantity", methods=["POST"])
def update_food_item_quantity():
    global food_production_department
    item_name = request.form.get("item_name")
    quantity = int(request.form.get("quantity"))

    # Update the food item quantity inside the lock
        # Update the food item quantity using food_production_department.update_quantity()
    food_production_department.update_quantity(item_name, quantity)
    food_production_department.display_food_items()

    response = {"message": "Quantity updated successfully"}
    return jsonify(response)

@app.route("/manager", methods=["GET"])
def manager():
    global c
    global food_production_department
    global food_items
    global customers
    customers = []
    cur = c.head
    while cur:
        status = False
        for i in range(len(customers)):
            if customers[i].get('customer_id') == cur.customer_id:
                status = True
                break
        if status:
            cur = cur.next
            continue
        customer = {
            'customer_id': cur.customer_id,
            'orders': []
        }
        order_cur = cur.order_head
        while order_cur:
            order = {
                'item_name': order_cur.item_name,
                'quantity': order_cur.quantity,
                'price': int(order_cur.price) * int(order_cur.quantity),
                'Payment': cur.payment,
                'Option': cur.option,
                'Verification': cur.verification

            }
            customer['orders'].append(order)
            order_cur = order_cur.next
        customers.append(customer)
        cur = cur.next

    # Fetch the food_items inside the lock
    with lock:
        food_items = food_production_department.get_food_items()

    return render_template("manager.html", customers=customers, food_items=food_items)


@app.route("/food_production_department")
def food_production_department_route():
    global food_items
    global customers

    # Fetch the food_items inside the lock
    with lock:
        food_items = food_production_department.get_food_items()
    print(food_items)
    print(customers)

    return render_template("food_production_department.html", food_items=food_items, customers=customers)


@app.route("/dequeue_customer", methods=["POST"])
def dequeue_customer():
    global c
    # Dequeue the front customer
    removed_customer = c.dequeue()
    if removed_customer is None:
        response = {"message": "No customer to dequeue"}
    else:
        response = {"message": "Customer dequeued successfully"}
    return jsonify(response)


@app.route("/decrease_linked_queue", methods=["POST"])
def decrease_linked_queue():
    global food_production_department
    item_name = request.form.get("item_name")

    # Decrease the quantity of the first element in the linked queue
    food_production_department.decrease_linked_queue(item_name)
    response = {"message": "Quantity of the first element decreased successfully"}
    return jsonify(response)

@app.route("/process_order", methods=["POST"])
def process_order():
    global c
    global customers
    data = request.get_json()
    customer_id = data.get('customer_id')
    item_name = data.get('item_name')
    cur = c.getCustomerNode(customer_id)
    send_email(emailg, "OTP", f"Here is your otp for verification : {cur.verification}\n\n\n{cur.display()}")
    print(customers)
    print("Mail is sent")
    response = {"message": "Order deleted successfully"}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
    sys.exit()