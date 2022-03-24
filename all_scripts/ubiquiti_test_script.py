from bs4 import BeautifulSoup
import requests
import json
import os
from twilio.rest import Client


def lambda_handler(event, context):
    print(context)
