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