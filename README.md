🚀 Telegram Auto Forwarder Bot 🤖

Welcome to Telegram Auto Forwarder Bot! This bot automatically forwards messages from one Telegram group to multiple other groups. No more copy-pasting messages manually! 🎉

🎯 Features

✅ Auto-Forward Messages: Forwards messages from a selected group to multiple groups.
✅ Group Selection: Choose which group to forward messages from dynamically.
✅ Periodic Resend: Re-sends the last forwarded message every 5 minutes.
✅ Error Handling: No more crashing! The bot handles errors gracefully.
✅ Multi-Group Support: Send messages to different groups using IDs or usernames.
✅ Easy Configuration: Just add your Telegram API credentials and start!

📦 Installation

1️⃣ Clone the repository

git clone https://github.com/ferx2006/Telegram-Shilling.git
cd Telegram-Shilling

2️⃣ Install dependencies

pip install -r requirements.txt

3️⃣ Set up your Telegram API credentials

You'll need to get api_id and api_hash from Telegram's Developer Portal.

Open config.py file and add your credentials:

API_ID=your_api_id
API_HASH=your_api_hash
PHONE_NUMBER=your_phone_number

4️⃣ Run the bot

python Shilling.py

🛠 How It Works

1. The bot asks you to select a group from your active chats.


2. Once selected, it listens for new messages in that group.


3. When a message is detected, it forwards it to the predefined groups.


4. Every 5 minutes, it resends the last forwarded message.



🚀 Boom! No more manual forwarding!

🔧 Upcoming Features

🔹 Message filtering (keywords, user-based, media types)
🔹 Support for forwarding from channels and private chats
🔹 Webhook support for integrations
🔹 Logging system instead of print()
🔹 Docker support for easy deployment

🎉 Contributing

Want to make this bot even cooler? Fork it, improve it, and submit a pull request!

1. Fork this repo 🚀


2. Create a new branch (feature-awesome-stuff)


3. Commit your changes (git commit -m "Added awesome feature")


4. Push and submit a PR



❤️ Support the Project

Give this repo a ⭐ if you like it!

💬 Questions? Issues? Open a GitHub issue or DM me on Telegram!
@Ferx2005