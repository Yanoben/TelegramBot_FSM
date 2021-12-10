import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
session_str = os.getenv('session_str')

# with TelegramClient(StringSession(), api_id, api_hash) as client:
#     print("Your session string is:", client.session.save())

client = TelegramClient(session_str, api_id=api_id, api_hash=api_hash)


async def print_message():
    message = await client.get_messages('TelethonSnippets', ids=3)
    print("MESSAGE:", end="\n-------\n")
    print(message.text)


with client:
    client.loop.run_until_complete(print_message())
