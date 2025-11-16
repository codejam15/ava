# import re
# import traceback
#
# from botbuilder.core import (
#     BotFrameworkAdapter,
#     BotFrameworkAdapterSettings,
#     TurnContext,
# )
# from botbuilder.schema import Activity
# from botframework.connector.auth import (
#     AuthenticationConfiguration,
#     MicrosoftAppCredentials,
#     SimpleCredentialProvider,
# )
# from fastapi import APIRouter, Request, Response
#
# from src.config import settings as s
#
# router = APIRouter()
#
# # ====== ADAPTER ======
#
#
# # Create auth config that allows unauthenticated requests (for testing)
# class AllowAllAuthConfig(AuthenticationConfiguration):
#     async def validate_claims(self, claims):
#         # Allow all claims for now
#         return
#
#
# # Create settings with relaxed auth
# credential_provider = SimpleCredentialProvider(
#     app_id="413eeb41-f381-4cca-b7cd-22a54cb17c37",
#     password=s.APP_PASSWORD,
# )
#
# settings = BotFrameworkAdapterSettings(
#     app_id="413eeb41-f381-4cca-b7cd-22a54cb17c37",
#     app_password=s.APP_PASSWORD,
#     auth_configuration=AllowAllAuthConfig(),
# )
#
# adapter = BotFrameworkAdapter(settings)
#
#
# def test_auth():
#     credentials = MicrosoftAppCredentials(
#         app_id="413eeb41-f381-4cca-b7cd-22a54cb17c37", password=s.APP_PASSWORD
#     )
#
#     try:
#         token = credentials.get_access_token()
#         print(f"✓ Authentication successful! Token: {token[:20]}...")
#         return True
#     except Exception as e:
#         print(f"✗ Authentication failed: {e}")
#         return False
#
#
# @router.post("/messages")
# async def messages(request: Request):
#     try:
#         body = await request.json()
#         auth_header = request.headers.get("Authorization", "")
#
#         print(auth_header)
#
#         # Deserialize activity
#         activity = Activity().deserialize(body)
#
#         print(f"Received: {activity.type}")
#         print(f"Service URL: {activity.service_url}")
#
#         # Debug: Check adapter credentials
#         print(f"Adapter App ID: {adapter.settings.app_id}")
#         print(f"Adapter has password: {bool(adapter.settings.app_password)}")
#
#         async def turn_handler(turn_context: TurnContext):
#             try:
#                 activity = turn_context.activity
#
#                 # Handle conversation updates
#                 if activity.type == "conversationUpdate":
#                     members_added = getattr(activity, "members_added", []) or []
#                     for member in members_added:
#                         if member.id != activity.recipient.id:
#                             await turn_context.send_activity(
#                                 "Thanks for installing AVA! Type 'Hi' to get started."
#                             )
#                     return
#
#                 # Handle messages
#                 if activity.type == "message":
#                     text = (activity.text or "").strip()
#                     text = re.sub(
#                         r"<at>.*?</at>", "", text, flags=re.IGNORECASE
#                     ).strip()
#
#                     print(f"User text: {text}")
#
#                     # Debug: Get the actual token being used
#                     connector = turn_context.turn_state.get(
#                         adapter.BOT_CONNECTOR_CLIENT_KEY
#                     )
#                     if connector:
#                         creds = connector.config.credentials
#                         print(f"Credentials App ID: {creds.microsoft_app_id}")
#                         print(
#                             f"Credentials has password: {bool(creds.microsoft_app_password)}"
#                         )
#
#                         # Try to get a token
#                         try:
#                             token = creds.get_access_token()
#                             print(f"✓ Got token for sending: {token[:30]}...")
#                         except Exception as token_err:
#                             print(f"✗ Failed to get token: {token_err}")
#
#                     if text.lower() in ("hi", "hello", "hey"):
#                         await turn_context.send_activity("Hi! I'm AVA. How can I help?")
#                     else:
#                         await turn_context.send_activity(f"You said: {text}")
#
#             except Exception as ex:
#                 print(f"[TURN HANDLER ERROR] {ex}")
#                 traceback.print_exc()
#
#         # Create TurnContext
#         context = TurnContext(adapter, activity)
#
#         # Create connector client with credentials
#         connector_client = await adapter.create_connector_client(activity.service_url)
#         context.turn_state[adapter.BOT_CONNECTOR_CLIENT_KEY] = connector_client
#
#         # Debug: verify connector has credentials
#         print(f"Created connector for: {activity.service_url}")
#         print(
#             f"Connector has credentials: {hasattr(connector_client.config, 'credentials')}"
#         )
#
#         # Run the turn handler
#         await adapter.run_pipeline(context, turn_handler)
#
#         return Response(status_code=200)
#
#     except Exception as e:
#         print(f"[ENDPOINT ERROR] {e}")
#         traceback.print_exc()
#         return Response(status_code=500)
