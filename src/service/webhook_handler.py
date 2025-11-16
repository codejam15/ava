import uvicorn
from fastapi import FastAPI, APIRouter, Header, status, HTTPException, Request
from typing import Optional

# --- 1. Router Setup ---
router = APIRouter(
    tags=["Webhooks"],
    prefix="/webhook"
)

# --- 2. Security Configuration ---
DRIVE_WEBHOOK_SECRET = "my-secret-verification-string-for-drive"

# --- 3. Webhook Handler ---
@router.post("/drive", status_code=status.HTTP_204_NO_CONTENT)
async def google_drive_webhook(
    request: Request,
    x_goog_channel_token: Optional[str] = Header(None, alias="X-Goog-Channel-Token"),
    x_goog_resource_state: Optional[str] = Header(None, alias="X-Goog-Resource-State")
):
    """
    Handles incoming push notifications from Google Drive API.
    Prints headers and body for debugging.
    """

    # Print everything immediately
    print("\n--- Webhook received ---", flush=True)
    print("Headers:", dict(request.headers), flush=True)
    body_bytes = await request.body()
    print("Body:", body_bytes.decode(), flush=True)
    print("X-Goog-Channel-Token:", x_goog_channel_token, flush=True)
    print("X-Goog-Resource-State:", x_goog_resource_state, flush=True)

    # Security check (skip if token missing, like initial sync)
    if x_goog_channel_token:
        if x_goog_channel_token != DRIVE_WEBHOOK_SECRET:
            print("SECURITY ALERT: Invalid channel token!", flush=True)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid channel token")

    # Handle sync
    if x_goog_resource_state == "sync":
        print("✅ Initial sync received.", flush=True)
        return

    # Handle actual changes
    elif x_goog_resource_state == "change":
        print("✨ File change detected!", flush=True)
        # Here you would call Drive API changes.list using token.json
        return

    else:
        print(f"Received other resource state: {x_goog_resource_state}", flush=True)
        return

# --- 4. Main FastAPI app ---
app = FastAPI(title="Drive Webhook Processor")
app.include_router(router)

# --- 5. Run server ---
if __name__ == "__main__":
    uvicorn.run(
        "webhook_handler:app",  # replace with your filename if different
        host="0.0.0.0",
        port=8000,
        reload=True,            # for development
        log_level="info"
    )
