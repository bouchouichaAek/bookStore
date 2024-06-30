# payments/chargily_service.py

import requests
from django.conf import settings

def create_invoice( amount,  back_url):
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {settings.CHARGILY_SECRET}',
    }
   
    data = {
         "amount": amount,
         "currency": "dzd",
         "success_url": back_url,
    }
    response = requests.post(settings.CHARGILY_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()  # Contains the invoice data
    else:
        response.raise_for_status()  # Raise an exception for any error response

