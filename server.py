import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException, Header

app = FastAPI()

SECRET_KEY = b"my_super_secret_warehouse_key"

@app.get("/")
def home():
    return {"status": "Webhook receiver service is online!"}

@app.post("/webhook")
async def receive_webhook(request: Request, x_signature: str = Header(None)):
    if not x_signature:
        raise HTTPException(status_code=401, detail="Missing X-Signature header")

    # Read raw request body bytes for HMAC check
    payload_bytes = await request.body()

    # Compute HMAC-SHA256 signature
    expected_signature = hmac.new(SECRET_KEY, payload_bytes, hashlib.sha256).hexdigest()

    # Secure constant-time string comparison
    if not hmac.compare_digest(expected_signature, x_signature):
        raise HTTPException(
            status_code=401, 
            detail="Invalid signature. Payload tampered or unauthorized."
        )

    payload = await request.json()
    print(f"[SUCCESS] Received verified payload: {payload}")
    return {"status": "success", "message": "Webhook payload verified and accepted"}