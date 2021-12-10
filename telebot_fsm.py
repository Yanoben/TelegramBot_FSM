import os
import telebot
import logging
from bot_transitions import Bot_transition
from dotenv import load_dotenv


load_dotenv()

token = os.getenv('token')

bot = telebot.TeleBot(token)
bot_tran = Bot_transition()

logging.basicConfig(
        level=logging.DEBUG,
        filename='main.log',
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
    )

conf_quests = {
    'big_cash': 'Вы хотите большую пиццу, оплата - наличкой?',
    'big_card': 'Вы хотите большую пиццу, оплата - картой?',
    'little_cash': 'Вы хотите маленькую пиццу, оплата - наличкой?',
    'little_card': 'Вы хотите маленькую пиццу, оплата - картой?'
}


@bot.message_handler(commands=['start', 'pizza'])
def start(message):
    bot_tran.new()  # Reload transition
    rmk = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    rmk.add(telebot.types.KeyboardButton('Большую'),
            telebot.types.KeyboardButton('Маленькую'))

    msg = bot.send_message(message.chat.id,
                           'Какую вы хотите пиццу? Большую или маленькую?',
                           reply_markup=rmk)
    bot.register_next_step_handler(msg, get_payment)


@bot.message_handler(content_types=['str', 'text'])
def get_payment(message):
    if bot_tran.state == 'start':
        if message.text.lower() == 'большую':
            bot_tran.big()
        elif message.text.lower() == 'маленькую':
            bot_tran.little()
        rmk = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        rmk.add(telebot.types.KeyboardButton('Наличкой'),
                telebot.types.KeyboardButton('Картой'))

        msg = bot.send_message(message.chat.id,
                               'Как вы будете платить?',
                               reply_markup=rmk)
        bot.register_next_step_handler(msg, get_conf)
    else:
        bot.send_message(message.chat.id, 'Type /pizza again')


@bot.message_handler(content_types=['str', 'text'])
def get_conf(message):
    if message.text.lower() == 'наличкой':
        bot_tran.cash()
    elif message.text.lower() == 'картой':
        bot_tran.card()
    rmk = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    rmk.add(telebot.types.KeyboardButton('Да'),
            telebot.types.KeyboardButton('Нет'))
    msg = bot.send_message(message.chat.id,
                           conf_quests.get(bot_tran.state),
                           reply_markup=rmk)
    bot.register_next_step_handler(msg, confirmed)


@bot.message_handler(content_types=['str', 'text'])
def confirmed(message):
    if message.text.lower() == 'да':
        bot.send_message(message.chat.id, 'Спасибо за заказ')
    if message.text.lower() == 'нет':
        bot.send_message(message.chat.id, 'Type /pizza or /start again')


def main():
    bot.polling()


if __name__ == '__main__':
    main()
