import base64
import json
import os
import re

from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext,
)
from botbuilder.schema import Activity
from fastapi import APIRouter, Request, Response

from src.config import settings as s

print("=== Bot runtime env/config ===")
print("s.APP_ID:", repr(s.APP_ID))
print("s.APP_PASSWORD length:", len(s.APP_PASSWORD) if s.APP_PASSWORD else None)

app_id = os.environ.get("MICROSOFT_APP_ID") or s.APP_ID
app_pwd = os.environ.get("MICROSOFT_APP_PASSWORD") or s.APP_PASSWORD
print("MICROSOFT_APP_ID from env:", repr(app_id))
print("MICROSOFT_APP_PASSWORD length from env:", len(app_pwd) if app_pwd else None)

is_guid = bool(
    re.match(
        r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
        str(app_id),
    )
)
print("APP_ID looks like GUID?", is_guid)
print("=== end env/config ===")

router = APIRouter()

# ====== ADAPTER ======

settings = BotFrameworkAdapterSettings(s.APP_ID, s.APP_PASSWORD)
adapter = BotFrameworkAdapter(settings)


def decode_jwt_no_verify(token: str) -> dict:
    """Decodes a JWT token without verifying its signature.
    This is useful for inspecting claims when debugging validation issues.
    """
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return {"error": "Invalid JWT format"}
        payload = parts[1]
        # Add padding if necessary
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload).decode())
    except Exception as e:
        return {"error": f"Failed to decode JWT payload: {e}"}


# ====== MESSAGE ROUTE ======
@router.post("/messages")
async def messages(request: Request):
    # Read raw body and headers
    body = await request.body()
    activity = Activity.deserialize(json.loads(body.decode()))

    # Auth header required for skill / channel validation
    auth_header = request.headers.get("Authorization", "")

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split("Bearer ")[1]
        claims = decode_jwt_no_verify(token)
        print("--- Incoming JWT Claims ---")
        print(json.dumps(claims, indent=2))
        print("---------------------------")
    else:
        print("No Bearer token found in Authorization header.")

    # Define turn handler logic
    async def turn_handler(turn_context: TurnContext):
        print("Running turn handler...")
        print(turn_context.activity)

        if turn_context.activity.type == "message":
            await turn_context.send_activity(f"You said: {turn_context.activity.text}")
        else:
            await turn_context.send_activity(
                f"Activity type '{turn_context.activity.type}' not supported."
            )

    # Process the incoming activity
    try:
        await adapter.process_activity(activity, auth_header, turn_handler)
        return Response(content="", status_code=200)
    except Exception as e:
        print(f"[ERROR] {e}")
        return Response(content="Internal Server Error", status_code=500)
