import asyncio
from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity

# ====== CONFIG ======
APP_ID = ""      # leave blank for local testing
APP_PASSWORD = ""  # leave blank for local testing

# Bot Logic
async def on_message(activity: Activity):
    text = activity.text or ""
    return Activity(
        type="message",
        text=f"You said: {text}"
    )

# ====== ADAPTER ======
settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(settings)

# ====== ENDPOINT ======
async def messages(req: web.Request) -> web.Response:
    body = await req.json()
    activity = Activity().deserialize(body)

    if activity.type == "message":
        response = await on_message(activity)
        return web.json_response(response.serialize())

    return web.Response(status=200)


# ====== SERVER ======
app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(app, port=3978)

