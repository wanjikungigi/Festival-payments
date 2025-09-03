
import requests
import base64
import datetime
from django.http import JsonResponse

def stk_push(request):
    consumer_key = "YOUR_CONSUMER_KEY"
    consumer_secret = "YOUR_CONSUMER_SECRET"
    shortcode = "YOUR_SHORTCODE"
    passkey = "YOUR_PASSKEY"
    phone_number = request.GET.get("phone")   # passed from Lovable
    amount = request.GET.get("amount")

    # 1. Get access token
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(auth_url, auth=(consumer_key, consumer_secret))
    access_token = response.json()['access_token']

    # 2. Create password
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = shortcode + passkey + timestamp
    password = base64.b64encode(data_to_encode.encode()).decode()

    # 3. STK push request
    stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://yourdomain.com/api/mpesa/callback",
        "AccountReference": "FestivalTicket",
        "TransactionDesc": "Ticket Payment"
    }
    res = requests.post(stk_url, json=payload, headers=headers)
    return JsonResponse(res.json())
