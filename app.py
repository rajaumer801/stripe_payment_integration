import json

import requests
import stripe
from flask import Flask, render_template, request

app = Flask(__name__)

# You can get your testing keys from Stripe Dashboard
STRIPE_PUB_KEY = "pk_test_ruV5HnCRK60euQ3rXa4hvCtK00CntLDLX5"
STRIPE_SECRET_KEY = "sk_test_DguhbS1MuR0G4U0EmSRZk8rN00GsFXmp6P"
STRIPE_CLIENT_ID = "ca_FfvT9m1Ya6bwkRl7SYVxRq5ui3N5e3wL"
stripe.api_key = STRIPE_SECRET_KEY

# Your Server(app) Endpoint(link) where data will be processed
# Use Ngrok to tunnel your localhost and add Ngrok generated url to your Stripe Connect account setting
# Example URL http://8444056a.ngrok.io/process
redirect_uri = "http:127.0.0.1:8000/process"

# unique value for identification and process data, also to avoid CSRF attacks
state = "abcdzxy"

# send this url to newly registered merchant after providing data, he will be redirected to your provided redirect_uri
# from where you can get the merchant account_id(stripe_user_id) which you can use to perform transfers
authorizeUri = "https://connect.stripe.com/express/oauth/authorize?client_id={}&state={}".format(STRIPE_CLIENT_ID,state)

@app.route('/')
def index():
    return render_template('index.html', key=STRIPE_PUB_KEY)


@app.route('/charge', methods=['POST'])
def charge():

    # amount in cents
    amount = 50000

    # create a new customer
    customer = stripe.Customer.create(
        email='sample@customer.com',
        source=request.form['stripeToken']
    )

    # charge customer
    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)

@app.route('/process', methods=['GET'])
def process():

    code = request.args['code']
    state = request.args['state']

    data = {
        "client_secret": STRIPE_SECRET_KEY,
        "code": code,
        "grant_type": "authorization_code"
    }

    r = requests.post(url="https://connect.stripe.com/oauth/token", data=data)
    response_data = json.loads(r.content.decode('utf-8'))

    # save merchant_id in DB to perform actions related to merchant account
    merchant_id = response_data['stripe_user_id']
    print(merchant_id)

    return render_template('register.html')

@app.route('/transfer', methods=['POST'])
def transfer():

    data = request.get_json()

    # amount in cents
    amount = 50000

    # transfer funds to merchant
    stripe.Transfer.create(
        amount=amount,
        currency="usd",
        destination=data['merchant_id']
    )


if __name__ == '__main__':
    app.run(port=8000)
