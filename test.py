import os
import telebot
from dotenv import load_dotenv


load_dotenv()

token = os.getenv('token')


def test_send_message(self):
    text = 'CI Test Message'
    tb = telebot.TeleBot(token)
    ret_msg = tb.send_message(CHAT_ID, text)
    assert ret_msg.message_id
