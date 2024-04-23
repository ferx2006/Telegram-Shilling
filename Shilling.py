from telethon.sync import TelegramClient, events
from telethon.tl.types import InputPeerChannel
import os

# List of group IDs where you want to send messages
group_ids = ['group_id_1', 'group_id_2', 'group_id_3']

# ID of the group from which you want to retrieve messages
source_group_id = 'source_group_id'

# Initialize the Telegram client
session_file = 'telegram_session'
if os.path.exists(session_file):
    client = TelegramClient(session_file, api_id, api_hash)
else:
    api_id = input("Enter your API ID: ")
    api_hash = input("Enter your API hash: ")
    phone_number = input("Enter your phone number (with country code): ")

    client = TelegramClient(session_file, api_id, api_hash)
    client.start(phone_number)

# Event handler for new messages in the source group
@client.on(events.NewMessage(chats=source_group_id))
async def forward_message(event):
    # Get the message text
    message_text = event.message.text

    # Resend the message to the specified groups
    for group_id in group_ids:
        try:
            await client.send_message(group_id, message_text)
            print(f"Message sent to {group_id}")
        except Exception as e:
            print(f"Failed to send message to {group_id}: {e}")

async def main():
    # Get the source group entity
    source_group_entity = InputPeerChannel(source_group_id, source_group_id)

    # Start listening for new messages in the source group
    await client.run_until_disconnected()

# Run the script
with client:
    client.loop.run_until_complete(main())
