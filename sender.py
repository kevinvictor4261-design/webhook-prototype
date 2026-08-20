import time
import httpx

BASE_URL = "http://127.0.0.1:8000"

def scan_badge(attendee_id: str):
    print(f"\n--- [SCANNING] Kiosk scanned badge for {attendee_id} ---")
    response = httpx.post(f"{BASE_URL}/checkin", json={"attendee_id": attendee_id})
    print(f"HTTP Status: {response.status_code}")
    print(f"Response: {response.json()}")

def print_current_states():
    response = httpx.get(f"{BASE_URL}/attendees")
    print("\n--- [DATABASE STATE] Current Attendee Statuses ---")
    for att_id, info in response.json().items():
        print(f"  * {att_id} ({info['name']}): {info['status']}")

if __name__ == "__main__":
    print("==================================================")
    print("   SOLSTICE EVENTS CO. - DAY 4 PIVOT TEST SUITE  ")
    print("==================================================")

    # 1. Display initial database state (all UNCHECKED)
    print_current_states()

    # 2. Test Attendee 1 - First Scan (Expect 200 OK + PENDING)
    scan_badge("ATT-001")

    # 3. Test Attendee 1 - Duplicate Scan while PENDING (Expect 409 Conflict)
    scan_badge("ATT-001")

    # 4. Wait for background print callback to arrive
    print("\n[WAITING] Pausing 4 seconds for vendor webhook callback...")
    time.sleep(4)

    # 5. Verify ATT-001 transitioned from PENDING to CHECKED_IN
    print_current_states()

    # 6. Test Attendee 1 - Duplicate Scan after CHECKED_IN (Expect 409 Conflict)
    scan_badge("ATT-001")

    # 7. Test Attendee 2 and Attendee 3 (Standard async flows)
    scan_badge("ATT-002")
    scan_badge("ATT-003")

    # 8. Wait for remaining callbacks to complete
    print("\n[WAITING] Pausing 4 seconds for remaining callbacks...")
    time.sleep(4)

    # 9. Final verification of all 3 attendees
    print_current_states()