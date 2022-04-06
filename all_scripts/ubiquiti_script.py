from bs4 import BeautifulSoup
import requests
import json
import os
from twilio.rest import Client


def lambda_handler(event, context):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    twilio_number = os.environ['TWILIO_PHONE_NUMBER']

    client = Client(account_sid, auth_token)

    all_products = [
        {
            'name': 'camera-g4-instant',
            'id': '7008238501977'
        },
        {
            'name': 'uvc-g4-doorbell',
            'id': '4684279218265'
        },
    ]

    for product in all_products:
        r = requests.get(f"https://store.ui.com/collections/unifi-protect/products/{product['name']}")
        soup = BeautifulSoup(r.content, "html.parser")

        all_scripts = soup.find_all('script')

        for script in all_scripts:
            if 'product:' and f'"id":{product["id"]}' in script.text:
                found_product = script

        for line in found_product:
            if 'product:' and f'"id":{product["id"]}' in line:
                answer = line

        answer = str(answer)

        if '"available":true' in answer:
            msg = f"{product['name']} is currently available"

            message = client.messages \
                .create(
                body=msg,
                from_=twilio_number,
                to='+18654408251'
            )

            print(f"Text message sent (Message: {message.body}. Error: {message.error_message})")
            continue

        elif '"available":false' in answer:
            msg = f"{product['name']} is currently sold out"

        else:
            msg = f"The status of {product['name']} is unavailable"

        print(f"Text message not sent (Message: {msg})")
