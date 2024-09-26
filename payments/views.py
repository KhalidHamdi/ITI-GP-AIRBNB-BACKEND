from django.shortcuts import render, redirect
from django.http import JsonResponse
from .paymob import *
# Callback view for Paymob's payment notifications
import hashlib
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import logging

def paymob(request):
    return render(request, 'payments/payment.html')

@csrf_exempt
def initiate_payment(request):
    if request.method == 'POST':
        amount_cents = 100000  # e.g., 10000 cents = 100 EGP
        token = get_paymob_token()
        order_id = create_order(token, amount_cents)
        payment_token = get_payment_key(token, order_id, amount_cents)
        iframe_url = card_payment(payment_token)

        return redirect(iframe_url)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


# @csrf_exempt
# def payment_callback(request):
#     if request.method == 'POST':
#         data = request.POST
#         hmac_secret = 'F20B4DCEC7EFFCD9EA451CA115CDBC11'
        
#         print("Payment received from server")
        
        
#         # Generate the HMAC for validation
#         hmac_calculated = hashlib.sha512(f"{hmac_secret}".encode()).hexdigest()

#         # Compare the received HMAC with the calculated HMAC
#         if data.get('hmac') == hmac_calculated:
#             # Process the payment (e.g., mark as paid in your DB)
#             return JsonResponse({'status': 'success'})
#         else:
#             # If HMAC validation fails
#             return JsonResponse({'status': 'failed', 'reason': 'HMAC validation failed'}, status=400)
#     elif request.method == 'GET':
#         print("Request method not supported for this request type ")
#         return JsonResponse({'error': 'Invalid request method'}, status=405)



# logger = logging.getLogger(__name__)

# @csrf_exempt
# def payment_callback(request):
#     if request.method == 'POST':
#         data = request.POST
#         logger.info(f"Received callback data: {json.dumps(data)}")
        
#         hmac_secret = 'F20B4DCEC7EFFCD9EA451CA115CDBC11'
#         hmac_calculated = hashlib.sha512(f"{hmac_secret}".encode()).hexdigest()

#         if data.get('hmac') == hmac_calculated:
#             # Log payment success and mark in DB
#             logger.info("Payment successful")
#             return JsonResponse({'status': 'success'})
#         else:
#             # Log failure
#             logger.error("HMAC validation failed")
#             return JsonResponse({'status': 'failed', 'reason': 'HMAC validation failed'}, status=400)
#     elif request.method == 'GET':
#         logger.info("Received GET request for callback status")
#         return render(request, 'payments/status.html')
#     else:
#         logger.info("Received unsupported request method")
#         return JsonResponse({'error': 'Invalid request method'}, status=405)


# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# import hashlib

# @csrf_exempt
# def payment_callback(request):
#     print(f"Request method: {request.method}")

#     if request.method == 'POST':
#         # Parse the data received from Paymob
#         data = request.POST

#         # Get your HMAC secret from Paymob dashboard
#         hmac_secret = 'F20B4DCEC7EFFCD9EA451CA115CDBC11'

#         # List of fields required for HMAC calculation
#         hmac_fields = [
#             'amount_cents', 'created_at', 'currency', 'error_occured',
#             'has_parent_transaction', 'id', 'integration_id', 'is_3d_secure',
#             'is_auth', 'is_capture', 'is_refunded', 'is_standalone_payment',
#             'is_voided', 'order', 'owner', 'pending', 'source_data_pan',
#             'source_data_sub_type', 'source_data_type', 'success'
#         ]

#         # Sort the data lexicographically by the keys and concatenate the values
#         concatenated_string = ''.join([str(data.get(field, '')) for field in hmac_fields])

#         # Calculate HMAC using SHA512
#         calculated_hmac = hashlib.SHA512(f'{hmac_secret}{concatenated_string}'.encode()).hexdigest()
#         # calculated_hmac = hash_hmac('SHA512', concatenated_string, hmac_secret)

#         # Compare with the HMAC received from Paymob
#         received_hmac = data.get('hmac')

#         if calculated_hmac == received_hmac:
#             # HMAC is valid, process the payment
#             # Example: mark payment as complete in your database
#             return JsonResponse({'status': 'success'})
#         else:
#             # HMAC does not match, return an error
#             return JsonResponse({'status': 'failed'}, status=400)

#     return JsonResponse({'status': 'invalid_method'}, status=405)

# import hmac
# import hashlib

# @csrf_exempt
# def payment_callback(request):
#     if request.method == 'POST':
#         # Handle the payment callback using POST data
#         data = request.POST.dict()
#         received_hmac = data.pop('hmac', None)
#         if not received_hmac:
#             return JsonResponse({'status': 'missing_hmac'}, status=400)

#         # Sort data and calculate HMAC
#         sorted_data = sorted(data.items())
#         concatenated_values = ''.join(str(value) for key, value in sorted_data)
#         hmac_secret = 'F20B4DCEC7EFFCD9EA451CA115CDBC11'
#         calculated_hmac = hmac.new(hmac_secret.encode(), concatenated_values.encode(), hashlib.sha512).hexdigest()

#         if received_hmac == calculated_hmac:
#             return JsonResponse({'status': 'success'})
#         else:
#             return JsonResponse({'status': 'hmac_verification_failed'}, status=400)

#     elif request.method == 'GET':
#         # Optionally handle GET requests for other cases or log the request
#         return JsonResponse({'status': 'method_not_allowed'}, status=405)

#     return JsonResponse({'status': 'invalid_method'}, status=405)

import hashlib
import hmac
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

# Secret key from your Paymob profile (use a secure way to store this in production)
SECRET_KEY = 'F20B4DCEC7EFFCD9EA451CA115CDBC11'

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        # Extract the data from the request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        # Retrieve HMAC from the request (for validation)
        received_hmac = request.GET.get('hmac')

        if not received_hmac:
            return JsonResponse({'status': 'error', 'message': 'Missing HMAC'}, status=400)

        # Calculate the HMAC from the received data
        calculated_hmac = calculate_hmac(data)

        # Verify the HMAC values match
        if received_hmac != calculated_hmac:
            return JsonResponse({'status': 'error', 'message': 'HMAC validation failed'}, status=400)

        # Process the transaction data
        success = data.get('success')
        transaction_id = data.get('id')
        amount_cents = data.get('amount_cents')
        order_id = data['order'].get('merchant_order_id')

        # Example: handle successful transaction
        if success:
            # Update your database to mark the transaction as successful
            print(f"Transaction {transaction_id} for Order {order_id} successfully processed.")

        return JsonResponse({'status': 'success', 'message': 'Transaction processed'}, status=200)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def calculate_hmac(data):
    # Ensure the order of keys matches exactly as per Paymob's required fields
    keys = [
        'amount_cents', 'created_at', 'currency', 'error_occured', 
        'has_parent_transaction', 'id', 'integration_id', 'is_3d_secure', 
        'is_auth', 'is_capture', 'is_refunded', 'is_standalone_payment', 
        'is_voided', 'order', 'owner', 'pending', 'source_data_pan', 
        'source_data_sub_type', 'source_data_type', 'success'
    ]

    # Ensure that 'order' is treated correctly (i.e., if it's not a dictionary)
    data['order'] = data.get('order', '')  # Ensure 'order' is not a nested object

    # Source data handling: some fields may be nested, ensure they are concatenated properly
    data['source_data_pan'] = data.get('source_data', {}).get('pan', '')
    data['source_data_sub_type'] = data.get('source_data', {}).get('sub_type', '')
    data['source_data_type'] = data.get('source_data', {}).get('type', '')

    # Sort the keys to ensure lexicographical order
    sorted_keys = sorted(keys)

    # Concatenate values in lexicographical order
    concatenated_string = ''.join(str(data.get(key, '')) for key in sorted_keys)

    # Log the concatenated string for debugging
    print(f"Concatenated string: {concatenated_string}")

    # Secret key (ensure it matches exactly the one set in Paymob)
    secret_key = 'F20B4DCEC7EFFCD9EA451CA115CDBC11'

    # Create the HMAC using SHA512
    hmac_result = hmac.new(secret_key.encode(), concatenated_string.encode(), hashlib.sha512).hexdigest()

    return hmac_result

# hmac=05caa54378124218ba18caafebb4d70c0e97da8ba6ec63ea52fe7fa325feff8d8e970501c9b57ec3d2cf2e2c6e04150fa9ce7917bb8d77dacdf58e3d5d073d39



# GET request handler for Paymob integration
def callback_status(request):
    # Handle the GET request for status update
    if request.method == 'GET':
        # Extract the data from the request
        data = request.GET.dict()

        # Retrieve HMAC from the request (for validation)
        received_hmac = request.GET.get('hmac')

        # Calculate the HMAC from the received data
        calculated_hmac = calculate_hmac(data)

        # Verify the HMAC values match
        if received_hmac != calculated_hmac:
            return JsonResponse({
                'status': 'error', 
                'message': 'HMAC validation failed',
                'data': data,
                'received_hmac': received_hmac,
                'calculated_hmac': calculated_hmac
            }, status=400)

        # Process the transaction data
        success = data.get('success')
        transaction_id = data.get('id')
        amount_cents = data.get('amount_cents')
        order_id = data.get('order')

        # Example: handle successful transaction
        if success:
            # Update your database to mark the transaction as successful
            print(f"Transaction {transaction_id} for Order {order_id} successfully processed.")

        return JsonResponse({'status': 'success', 'message': 'Transaction processed'}, status=200)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

# import hashlib
# import hmac
# import json
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view

# @csrf_exempt
# def payment_callback(request):
#     if request.method == 'POST':
#         # Extract the data from the request
#         data = json.loads(request.body)

#         # Retrieve HMAC from the request (for validation)
#         received_hmac = request.GET.get('hmac')

#         # Calculate the HMAC from the received data
#         calculated_hmac = calculate_hmac(data)

#         # Verify the HMAC values match
#         if received_hmac != calculated_hmac:
#             return JsonResponse({'status': 'error', 'message': 'HMAC validation failed'}, status=400)

#         # Process the transaction data
#         success = data.get('success')
#         transaction_id = data.get('id')
#         amount_cents = data.get('amount_cents')
#         order_id = data['order'].get('merchant_order_id')

#         # Example: handle successful transaction
#         if success:
#             # Update your database to mark the transaction as successful
#             # For example, mark the order as paid
#             print("Transaction successfully add in database")

#         return JsonResponse({'status': 'success', 'message': 'Transaction processed'}, status=200)
#     else:
#         print("Transaction failed to add in database")
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    

# def calculate_hmac(data):
#     # Sort the keys and concatenate the values in lexicographical order
#     keys = ['amount_cents', 'created_at', 'currency', 'error_occured', 'has_parent_transaction', 'id',
#             'integration_id', 'is_3d_secure', 'is_auth', 'is_capture', 'is_refunded', 'is_standalone_payment', 
#             'is_voided', 'order.id', 'owner', 'pending', 'source_data.pan', 'source_data.sub_type', 
#             'source_data.type', 'success']
#     keys2 = [
#             'amount_cents', 'created_at', 'currency', 'error_occured',
#             'has_parent_transaction', 'id', 'integration_id', 'is_3d_secure',
#             'is_auth', 'is_capture', 'is_refunded', 'is_standalone_payment',
#             'is_voided', 'order', 'owner', 'pending', 'source_data_pan',
#             'source_data_sub_type', 'source_data_type', 'success'
#         ]
#     keys3 = [
#             'amount_cents', 'created_at', 'currency', 'error_occured',
#             'has_parent_transaction', 'id', 'owner', 'pending','source_data_pan',
#             'source_data_sub_type', 'source_data_type', 'success'
#         ]
    
#     sorted_keys = sorted(keys2)

#     concatenated_string = ''.join(str(data.get(key, '')) for key in sorted_keys)
    
#     print(f"Concatenated string: {concatenated_string}")

#     # Secret key from your Paymob profile
#     secret_key = 'F20B4DCEC7EFFCD9EA451CA115CDBC11'

#     # Create HMAC using SHA512
#     hmac_result = hmac.new(secret_key.encode(), concatenated_string.encode(), hashlib.sha512).hexdigest()

#     return hmac_result




# # GET Request in Paymob integration 
# # tell the client that the transaction has been received
# def callback_status(request):
#     # Handle the GET request for status update
#     if request.method == 'GET':
#         # Example: Update the transaction status in your database
#         # Example: Send an email or SMS notification to the client
#         # Example: Redirect to a success page or handle the transaction in your app
#          # Extract the data from the request
#         # data = json.loads(resp)
#         data = request.GET.dict()
#         # Retrieve HMAC from the request (for validation)
#         received_hmac = request.GET.get('hmac')

#         # Calculate the HMAC from the received data
#         calculated_hmac = calculate_hmac(data)

#         # Verify the HMAC values match
#         if received_hmac != calculated_hmac:
#             return JsonResponse({'status': 'error', 'message': 'HMAC validation failed', 'data' : data, 'received_hmac': received_hmac, 'calculated_hmac' : calculated_hmac}, status=400)

#         # Process the transaction data
#         success = data.get('success')
#         transaction_id = data.get('id')
#         amount_cents = data.get('amount_cents')
#         order_id = data['order'].get('merchant_order_id')

#         # Example: handle successful transaction
#         if success:
#             # Update your database to mark the transaction as successful
#             # For example, mark the order as paid
#             print("Transaction successfully add in database")

#         return JsonResponse({'status': 'success', 'message': 'Transaction processed'}, status=200)
#         # return JsonResponse({'status':'success'})

#     return JsonResponse({'status': 'invalid_method'}, status=405)
#     # print(request)
#     # return render(request, 'payments/status.html')

