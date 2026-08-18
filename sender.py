import hmac
import hashlib
import json
import requests

URL = "http://localhost:8000/webhook"
SECRET_KEY = b"my_super_secret_warehouse_key"

# Sample inventory update payload
data = {
    "item_id": "SKU-9942",
    "item_name": "Wireless Mouse",
    "stock_count": 120
}

payload_bytes = json.dumps(data).encode('utf-8')
signature = hmac.new(SECRET_KEY, payload_bytes, hashlib.sha256).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature": signature
}

# Test 1: Send valid signature
print("--- Sending Valid Webhook ---")
response = requests.post(URL, data=payload_bytes, headers=headers)
print(f"Status: {response.status_code} | Response: {response.text}\n")

# Test 2: Send invalid signature
print("--- Sending Tampered Webhook ---")
bad_headers = {"Content-Type": "application/json", "X-Signature": "fake_invalid_signature_123"}
bad_response = requests.post(URL, data=payload_bytes, headers=bad_headers)
print(f"Status: {bad_response.status_code} | Response: {bad_response.text}")