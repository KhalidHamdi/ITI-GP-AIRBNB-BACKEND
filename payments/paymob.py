# payments/paymob.py
import requests
from project.settings import PAYMOB_API_KEY, PAYMOB_INTEGRATION_ID

def get_paymob_token():
    url = "https://accept.paymob.com/api/auth/tokens"
    data = {"api_key": PAYMOB_API_KEY}
    response = requests.post(url, json=data)
    return response.json().get('token')

def create_order(token, amount_cents):
    url = "https://accept.paymob.com/api/ecommerce/orders"
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        "amount_cents": amount_cents,
        "currency": "EGP",
        "items": []
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json().get('id')

def get_payment_key(token, order_id, amount_cents):
    url = "https://accept.paymob.com/api/acceptance/payment_keys"
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        "amount_cents": amount_cents,
        "currency": "EGP",
        "order_id": order_id,
        "billing_data": {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@test.com",
            "phone_number": "+201011234567",
            "apartment": "NA",
            "floor": "NA",
            "street": "NA",
            "building": "NA",
            "city": "Cairo",
            "country": "EG",
            "state": "NA"
        },
        "integration_id": PAYMOB_INTEGRATION_ID
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json().get('token')


# Usage
def card_payment(payment_token):
    iframe_url = f'https://accept.paymob.com/api/acceptance/iframes/869507?payment_token={payment_token}'
    return iframe_url


