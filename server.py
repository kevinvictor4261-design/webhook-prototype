import hmac
import hashlib
import asyncio
import httpx
from fastapi import FastAPI, Header, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel

app = FastAPI(title="Solstice Events Kiosk & Webhook Server")

SECRET_KEY = b"my_super_secret_warehouse_key"

# In-memory state tracking store
attendees_db = {
    "ATT-001": {"name": "Alice Johnson", "status": "UNCHECKED"},
    "ATT-002": {"name": "Bob Smith", "status": "UNCHECKED"},
    "ATT-003": {"name": "Charlie Davis", "status": "UNCHECKED"},
}

class CheckInRequest(BaseModel):
    attendee_id: str

# Helper function: Simulates the external badge printer vendor processing asynchronously
async def simulate_vendor_printer_callback(attendee_id: str):
    await asyncio.sleep(3)  # Simulate 3-second print delay at venue
    
    # Construct signed payload to send back to our webhook receiver
    raw_payload = f'{{"attendee_id":"{attendee_id}","status":"success"}}'.encode("utf-8")
    signature = hmac.new(SECRET_KEY, raw_payload, hashlib.sha256).hexdigest()

    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                "http://127.0.0.1:8000/webhook/print-status",
                content=raw_payload,
                headers={
                    "Content-Type": "application/json",
                    "X-Signature": signature
                }
            )
        except Exception as e:
            print(f"Error delivering webhook callback: {e}")

# --- Kiosk Scan Endpoint ---
@app.post("/checkin")
def check_in_attendee(request: CheckInRequest, background_tasks: BackgroundTasks):
    attendee = attendees_db.get(request.attendee_id)

    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee non-existent.")

    # Duplicate scan protection
    if attendee["status"] == "PENDING":
        raise HTTPException(
            status_code=409, 
            detail="Scan rejected: Badge print already in progress for this attendee."
        )
    if attendee["status"] == "CHECKED_IN":
        raise HTTPException(
            status_code=409, 
            detail="Scan rejected: Attendee is already checked in and badge printed."
        )

    # Update state to PENDING immediately and queue background print job
    attendee["status"] = "PENDING"
    background_tasks.add_task(simulate_vendor_printer_callback, request.attendee_id)

    return {
        "status": "PENDING",
        "message": f"Print job queued for {attendee['name']}. Awaiting printer callback."
    }

# --- Webhook Callback Endpoint ---
@app.post("/webhook/print-status")
async def handle_print_webhook(request: Request, x_signature: str = Header(None)):
    if not x_signature:
        raise HTTPException(status_code=401, detail="Missing X-Signature header.")

    raw_body = await request.body()
    computed_signature = hmac.new(SECRET_KEY, raw_body, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(computed_signature, x_signature):
        raise HTTPException(status_code=401, detail="Invalid HMAC signature.")

    data = await request.json()
    attendee_id = data.get("attendee_id")
    print_status = data.get("status")

    if attendee_id in attendees_db and print_status == "success":
        attendees_db[attendee_id]["status"] = "CHECKED_IN"
        print(f"[WEBHOOK EVENT] Badge printed successfully for {attendee_id}. State -> CHECKED_IN")

    return {"status": "success", "message": "State updated via async callback"}

# --- Status Query Endpoint ---
@app.get("/attendees")
def list_attendees():
    return attendees_db