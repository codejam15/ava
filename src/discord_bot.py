import discord
from discord.channel import TextChannel

CHANNEL_ID = 0

# --- Bot Setup ---

# Define the 'intents' for your bot. These are permissions for what
# your bot needs to be able to "see" or "do".
intents = discord.Intents.default()
intents.guilds = True  # To see server information
intents.messages = True  # To see messages
intents.message_content = True  # To read the content of messages

# Create the bot client
client = discord.Client(intents=intents)

# --- Bot Events ---
 
async def send_personalized_feedback(id:int, message: str):
    user = client.get_user(id)
    if user == None:
        print("Could not fined user")
    else:
        try:
            await user.send(message)
            print(f"Sent DM to {user.name}")
        except discord.Forbidden:
            print(f"Could not send DM to  {user.name} They might have DMs disabled.")
        except Exception as e:
            print(f"An error occurred: {e}")

async def post_meeting_minutes(meeting_minutes: str):

    # channel id
    channel = client.get_channel(CHANNEL_ID)

    if channel and isinstance(channel, TextChannel):
        try:
            await channel.send(meeting_minutes)

        except Exception as e:
            print(f"Exception occurred: {e}")


@client.event
async def on_ready():
    """
    This event is triggered when the bot successfully connects to Discord.
    """
    print(f"Bot is ready! Logged in as {client.user}")
    print("-------------------------------------------")


@client.event
async def on_message(message):
    """
    This event is triggered for every message sent in any channel
    the bot can see.
    """
    if message.author == client.user:
        return

    global CHANNEL_ID

    if message.content == "!postminutes":
        try:
            await post_meeting_minutes("Hello these are meeting minutes")
        except Exception as e:
            print(f"There was an error {e}")

    if message.content == "!setmeetingchannel":
        try:
            id = message.channel.id
            CHANNEL_ID = id
            await message.channel.send(
                f"Successfully set Ava's server to {message.channel.name}"
            )

        except Exception as e:
            print(f"An error occurred {e}")
