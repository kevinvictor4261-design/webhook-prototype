# Assignment 1: Learning & Blocker Journal

**Language:** Python 3  
**Unfamiliar Concept Chosen:** Webhook Verification (HMAC-SHA256)

---

## Blocker Log & Progress Timeline

| Time / Date | Issue / Error Encountered | Resource Consulted | Resolution |
| :--- | :--- | :--- | :--- |
| *Aug 18, 12:15 PM* | `python3` command not recognized on Windows | Python official docs | Windows uses `python` or `py`. |
| *Aug 18, 12:20 PM* | `No module named venv` | Terminal syntax check | Fixed typo in environment creation command. |
| *Aug 18, 12:45 PM* | `127.0.0.1:8000` infinite loading in browser | Windows network loopback behavior | Switched to `http://localhost:8000` and updated Uvicorn host flag. |
## Personal Reflection & Learning Outcomes

> I have been able to try and do the task while learning as I go. I have learned Git commands and Python commands and applied them practically. My project may not be perfect, but I have gained significant hands-on experience and understanding from completing this task.

## Day 4: Meridian Pivot — Asynchronous Check-In & Duplicate Scan Protection

### Overview & Architecture Pivot
Pivoted the Solstice Events Co. kiosk service from a synchronous REST architecture to an asynchronous event-driven model following vendor API deprecation. Rather than holding HTTP requests while waiting for physical badge printing, the system now registers requests immediately, emits a background print task, and transitions attendee state asynchronously via authenticated webhook callbacks.

### Implementation Details
* **State Management:** Added in-memory tracking for attendee lifecycle states (`UNCHECKED`, `PENDING`, `CHECKED_IN`).
* **Non-Blocking Check-In (`POST /checkin`):** Receives QR scans, sets status to `PENDING`, and queues background execution for vendor print simulation while instantly releasing the kiosk UI.
* **Duplicate Scan Guard:** Enforced concurrency protection by returning HTTP `409 Conflict` if a scan occurs for an attendee currently in `PENDING` or `CHECKED_IN` status.
* **Callback Handler (`POST /webhook/print-status`):** Reused HMAC-SHA256 signature validation from earlier iterations to verify incoming vendor completion payloads before advancing state to `CHECKED_IN`.

### Testing & Verification
Executed `sender.py` simulating 3 attendee workflows and edge cases:
1. **Initial Scan (`ATT-001`):** Returned `200 OK` with status `PENDING`.
2. **Duplicate Scan Prevention:** Rapid secondary scan of `ATT-001` while `PENDING` correctly triggered `409 Conflict` ("Badge print already in progress").
3. **Async Callback Completion:** Vendor simulation delivered signed webhook; status updated to `CHECKED_IN`.
4. **Post-Checkin Duplicate Scan:** Secondary scan of `ATT-001` after completion correctly triggered `409 Conflict` ("Attendee is already checked in").
5. **Multi-Attendee Delivery:** Processed `ATT-002` and `ATT-003` concurrently through the full asynchronous lifecycle.

### Reflection
Covering day 4 has been a bit tricky because we had changes to make on this very day from what we had created on the previous days. I have seen what happens to provide such responses and all i have done is try and take notes on the commands i have had to use and i also want read the codes and understand what happens.