# from flask import Flask, render_template, url_for
# import pyqrcode
# import os
# import uuid

# app = Flask(__name__)

# def generate_payment_url(order_id, amount):
#     # This is a mock function to generate a unique payment URL
#     # In a real-world scenario, this would integrate with your payment system
#     base_url = "https://payment.example.com/checkout"
#     return f"{base_url}?order_id={order_id}&amount={amount}"

# @app.route('/checkout/<order_id>')
# def checkout(order_id):
#     # Generate a unique payment URL for the order
#     amount = 50  # This would be calculated based on the order details
#     payment_url = generate_payment_url(order_id, amount)
#     qr = pyqrcode.create(payment_url)
#     qr_code_path = os.path.join('static', f'payment_qr_{order_id}.png')
#     qr.png(qr_code_path, scale=8)

#     # Render the checkout page with the QR code
#     return render_template('checkout.html', qr_code_url=url_for('static', filename=f'payment_qr_{order_id}.png'))

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, render_template, url_for, request
# import pyqrcode
# import os

# app = Flask(__name__)

# @app.route('/')
# def home():
#     # Get the order ID from the query parameter
#     order_id = request.args.get('order_id')

#     # Generate a unique payment URL for the order
#     payment_url = f"https://payment.example.com/checkout?amount=50&order_id={order_id}"
#     qr = pyqrcode.create(payment_url)
#     qr_code_path = os.path.join('static', f'payment_qr_{order_id}.png')
#     qr.png(qr_code_path, scale=8)

#     # Render the home page with the QR code
#     return render_template('index.html', qr_code_url=url_for('static', filename=f'payment_qr_{order_id}.png'))

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, render_template, url_for
# import pyqrcode
# import os
# import jwt
# import datetime

# app = Flask(__name__)
# SECRET_KEY = '6d0e30d209c8eabc2a07e8b91f9bbd0d1f8c88b42c68a5c3190e56fda1a36e7c'  # Replace with your secret key

# def generate_payment_url(order_id, amount, expiration_time):
#     # Generate a unique payment URL for each transaction with an expiration time
#     token = jwt.encode({
#         'order_id': order_id,
#         'amount': amount,
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration_time)
#     }, SECRET_KEY, algorithm='HS256')
#     return f"https://payment.example.com/checkout?token={token}"

# @app.route('/checkout/<int:order_id>')
# def checkout(order_id):
#     # Get the cart details or order amount
#     # For simplicity, we'll use a fixed amount
#     amount = 50
#     expiration_time = 300  # Link expires in 5 minutes (300 seconds)

#     # Generate a unique payment URL with expiration
#     payment_url = generate_payment_url(order_id, amount, expiration_time)

#     # Generate a QR code for the payment URL
#     qr = pyqrcode.create(payment_url)
#     qr_code_path = os.path.join('static', f'payment_qr_{order_id}.png')
#     qr.png(qr_code_path, scale=8)

#     # Render the checkout page with the QR code
#     return render_template('index.html', qr_code_url=url_for('static', filename=f'payment_qr_{order_id}.png'))

# if __name__ == '__main__':
#     app.run(debug=True)

# import secrets
# secret_key = secrets.token_hex(32)
# print(secret_key)


from flask import Flask, render_template, request, redirect, url_for
import pyqrcode
import os
import jwt
import datetime

app = Flask(__name__)
SECRET_KEY = '5c6bcf338594d5e29a21c11b4c941a1d3a66f396350911f98b7933e42fa06dae'  # Replace with your secret key

# Define a list of items and their prices
ITEMS = {
    'item1': 10,
    'item2': 15,
    'item3': 20,
    'item4': 25
}

def generate_payment_url(order_id, items, expiration_time):
    # Calculate the total amount
    total_amount = sum(ITEMS[item] for item in items)
    # Generate a unique payment URL for each order with an expiration time
    token = jwt.encode({
        'order_id': order_id,
        'items': items,
        'total_amount': total_amount,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration_time)
    }, SECRET_KEY, algorithm='HS256')
    return f"https://payment.example.com/checkout?token={token}"

@app.route('/')
def index():
    # Display the available items
    return render_template('index.html', items=ITEMS.keys())

@app.route('/checkout', methods=['POST'])
def checkout():
    # Get the selected items from the form
    selected_items = request.form.getlist('items')
    order_id = str(uuid.uuid4())  # Generate a unique order ID
    expiration_time = 300  # Link expires in 5 minutes (300 seconds)

    # Generate a unique payment URL with expiration
    payment_url = generate_payment_url(order_id, selected_items, expiration_time)

    # Generate a QR code for the payment URL
    qr = pyqrcode.create(payment_url)
    qr_code_path = os.path.join('static', f'payment_qr_{order_id}.png')
    qr.png(qr_code_path, scale=8)

    # Render the checkout page with the QR code
    return render_template('checkout.html', qr_code_url=url_for('static', filename=f'payment_qr_{order_id}.png'))

if __name__ == '__main__':
    app.run(debug=True)