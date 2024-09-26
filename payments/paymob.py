# payments/paymob.py
import requests
PAYMOB_API_KEY = 'ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2T1RrMk5ETTJMQ0p1WVcxbElqb2lhVzVwZEdsaGJDSjkuWnc2WEcyVGYybkxSNE83b0wwai1Ea1FESzVFYlNaSVh5dFBTLUNSZHpkQTk1V29RRjYzTlQ0SFRmeFRjMWZ4SHNKWVB4WERtVXJKVjBzMHZtY3VILVE='
PAYMOB_INTEGRATION_ID = '4836448'

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
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@example.com",
            "phone_number": "+201234567890",
            "apartment": "803",
            "floor": "42",
            "building": "123",
            "street": "Sample Street",
            "city": "Cairo",
            "country": "EG",
            "postal_code": "12345"
        },
        "integration_id": PAYMOB_INTEGRATION_ID
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json().get('token')


# Usage
def card_payment(payment_token):
    iframe_url = f'https://accept.paymob.com/api/acceptance/iframes/869507?payment_token={payment_token}'
    return iframe_url


