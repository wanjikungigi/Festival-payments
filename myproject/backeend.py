import requests
import base64
import datetime
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Add this if you're making POST requests from external sources
def stk_push(request):
    # 1. Get credentials from environment
    consumer_key = os.environ.get('CONSUMER_KEY')
    consumer_secret = os.environ.get('CONSUMER_SECRET')
    shortcode = os.environ.get('SHORTCODE', '174379')  # default to sandbox
    passkey = os.environ.get('PASSKEY', 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919')
    
    # 2. Get and validate parameters
    phone_number = request.GET.get("phone")
    amount = request.GET.get("amount")
    
    if not phone_number or not amount:
        return JsonResponse({"error": "Phone and amount are required"}, status=400)
    
    try:
        # 3. Format phone number
        phone_number = phone_number.replace("+", "").replace(" ", "")
        if not phone_number.startswith("254"):
            if phone_number.startswith("0"):
                phone_number = "254" + phone_number[1:]
            else:
                phone_number = "254" + phone_number
        
        # 4. Get access token
        auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(auth_url, auth=(consumer_key, consumer_secret))
        
        if response.status_code != 200:
            return JsonResponse({"error": "Failed to get access token"}, status=500)
            
        access_token = response.json().get('access_token')
        if not access_token:
            return JsonResponse({"error": "No access token received"}, status=500)
        
        # 5. Create password
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        data_to_encode = shortcode + passkey + timestamp
        password = base64.b64encode(data_to_encode.encode()).decode()

        # 6. STK push request
        stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {
            "BusinessShortCode": shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://your-app-name.onrender.com/api/mpesa/callback",  # UPDATE THIS
            "AccountReference": "FestivalTicket",
            "TransactionDesc": "Ticket Payment"
        }
        
        res = requests.post(stk_url, json=payload, headers=headers)
        return JsonResponse(res.json())
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)