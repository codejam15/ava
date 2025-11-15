from botbuilder.core import ActivityHandler, TurnContext

class MyBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text
        await turn_context.send_activity(f"You said: {user_message}")

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        await turn_context.send_activity("Bot is online.")

