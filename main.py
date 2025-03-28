import os
from dotenv import load_dotenv
from pyrogram import Client, filters

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables and ensure they are set
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

# Check if any variable is missing
if not all([api_id, api_hash, bot_token]):
    raise ValueError("Missing API_ID, API_HASH, or BOT_TOKEN in environment variables")

# Convert API ID to int
api_id = int(api_id)

app = Client("mention_all_bot", api_id, api_hash, bot_token=bot_token)

@app.on_message(filters.command("mentionall", prefixes=["/", "!"]) & filters.group)
async def mention_all(client, message):
    chat_id = message.chat.id
    mentions = []

    # Get all members in the group
    async for member in client.get_chat_members(chat_id):
        if not member.user.is_bot:
            if member.user.username:  # If user has a username
                mention = f"@{member.user.username}"
            else:  # If user has no username, mention by ID
                mention = f"[{member.user.first_name}](tg://user?id={member.user.id})"
            mentions.append(mention)

    # Prepare the mention text, ensure it does not exceed 4096 characters
    if mentions:
        mention_text = " ".join(mentions)

        # Telegram message limit is 4096 characters
        if len(mention_text) > 4096:
            mention_text = "Too many users to mention at once."

        await message.reply_text(mention_text, disable_web_page_preview=True, parse_mode="HTML")
    else:
        await message.reply_text("No users found!")

app.run()
