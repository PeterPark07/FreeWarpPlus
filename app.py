from datetime import datetime
from json import dumps
from random import choice, randint
from string import ascii_letters, digits
from time import sleep
import httpx
import os
from flask import Flask, request

app = Flask(__name__)
warp_client_id = os.getenv('warp_id')

# Defaults
success_count, fail_count = 0, 0

def generate_string(length):
  try:
    letters_and_digits = ascii_letters + digits
    return ''.join(choice(letters_and_digits) for _ in range(length))
  except Exception as error_code:
    print(error_code)

def generate_digit_string(length):
  try:
    digits_only = digits
    return ''.join(choice(digits_only) for _ in range(length))
  except Exception as error_code:
    print(error_code)

url = f"https://api.cloudflareclient.com/v0a{generate_digit_string(3)}/reg"

@app.route('/')
def add_5_gbs():
  client_ip = request.remote_addr  # Get the IP address of the client
  print(f"Hit by IP: {client_ip}")
  global success_count, fail_count
  for i in range(5):
    try:
      install_id = generate_string(22)
      body = {
        "key": f"{generate_string(43)}=",
        "install_id": install_id,
        "fcm_token": f"{install_id}:APA91b{generate_string(134)}",
        "referrer": warp_client_id,
        "warp_enabled": False,
        "tos": f"{datetime.now().isoformat()[:-3]}+02:00",
        "type": "Android",
        "locale": "es_ES"
      }
      data = dumps(body).encode("utf8")
      headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "api.cloudflareclient.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.1"
      }
      response = httpx.post(url, data=data, headers=headers).status_code
    except Exception as error_code:
      print(error_code)

    if response == 200:
      success_count += 1
      print(f"PASSED: +1GB (total: {success_count}GB, failed: {fail_count})")
    else:
      print(f"FAILED: {response}")
      fail_count += 1
    
    # Cooldown
    cooldown_time = randint(30, 50)
    print(f"Sleep: {cooldown_time} seconds.")
    sleep(cooldown_time)
  
  return "Adding 5GB to your account."

if __name__ == '__main__':
    app.run()
