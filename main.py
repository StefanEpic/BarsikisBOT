import telebot
from utils import get_news, Menu, Weather, Horoscope, Currency
from games import GameSpoke, GameTicTacToe
from config import tkn

bot = telebot.TeleBot(tkn)
menu = Menu()
weather = Weather()
horo = Horoscope()
cur = Currency()
battle = GameSpoke()
tic = GameTicTacToe()


@bot.message_handler(commands=['start'])
def handle_start(message):
    sti = open('welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, f'Мяу, Мяу-Мяу, {message.chat.first_name}!', reply_markup=menu.keyboard)


@bot.message_handler(content_types=['text'])
def handle_weather(message):
    global weather, horo, cur, battle, tic

    if message.chat.type == 'private':
        if message.text == '\U0001F326 Погода':
            bot.send_message(message.chat.id, f'Выберите ваш город:', reply_markup=weather.keyboard)
        elif message.text == '\U0001F525 Новости':
            bot.send_message(message.chat.id, f'\U0001F525 Актуальные новости от "Lenta.ru":\n{get_news()}',
                             parse_mode='Markdown')
        elif message.text == '\U00002651 Гороскоп':
            bot.send_message(message.chat.id, f'Выберите свой знак зодиака:', reply_markup=horo.keyboard)
        elif message.text == '\U0001F4B1 Конвертация валюты':
            bot.send_message(message.chat.id, f'\U0001F4B1 Курсы валют:\n{cur.start_currency()}')
            bot.send_message(message.chat.id, f'Из какой валюты переводим?',
                             reply_markup=cur.keyboard_from)
        elif message.text == '\U0001F3AE Мини-игры':
            bot.send_message(message.chat.id,
                             f'В какую игру будем играть?\n\U0001F596 Камень, ножницы, бумага, ящерица, Спок\n\U0000274C Крестики-Нолики',
                             reply_markup=menu.game_keyboard)

        if cur.currency_mode:
            if len(message.text.split()) > 1:
                bot.send_message(message.chat.id, f'Должно быть одно число!')
            else:
                try:
                    amount = float(message.text)
                    bot.send_message(message.chat.id, f'{cur.get_currency(amount)}')
                    cur.currency_mode = False
                except ValueError:
                    bot.send_message(message.chat.id, f'Пожалуйста, введите число!')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global weather, horo, cur, battle, tic

    if call.data in weather.dict_city.keys():
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        bot.send_message(call.message.chat.id, weather.get_weather(call.data))
    elif call.data in horo.dict_horo.keys():
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        bot.send_message(call.message.chat.id, f'{horo.dict_horo[call.data]}\n{horo.get_horo()[int(call.data)]}')
    elif call.data in cur.cur_list_from:
        cur.from_ = call.data[5:]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'В какую валюту переводим?', reply_markup=cur.keyboard_to)
    elif call.data in cur.cur_list_to:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        cur.to_ = call.data[3:]
        cur.currency_mode = True
        bot.send_message(call.message.chat.id, f'Введите сумму:')
    elif call.data == 'Ящерица-Спок':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        battle.sti = open('game_start_spoke.webp', 'rb')
        bot.send_sticker(call.message.chat.id, battle.sti)
        battle = GameSpoke(call.message.chat.first_name, '', 5, 5, '')
        bot.send_message(call.message.chat.id, battle, reply_markup=battle.keyboard)
    elif call.data == 'Крестики-Нолики':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        tic.sti = open('game_start_tictactoe.webp', 'rb')
        bot.send_sticker(call.message.chat.id, tic.sti)
        tic = GameTicTacToe()
        bot.send_message(call.message.chat.id, tic, reply_markup=tic.keyboard)
    elif call.data in battle.items:
        battle.move(call.data)
        if battle.game_win == 'AI':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
            bot.send_sticker(call.message.chat.id, battle.sti)
            bot.send_message(call.message.chat.id, f'You lose!')
        elif battle.game_win == 'Player':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
            bot.send_sticker(call.message.chat.id, battle.sti)
            bot.send_message(call.message.chat.id, f'You win!')
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=battle,
                                  reply_markup=battle.keyboard)
    elif call.data in tic.items:
        tic.move(call.data)
        if tic.game_win == 'Player':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
            bot.send_sticker(call.message.chat.id, tic.sti)
            bot.send_message(call.message.chat.id, f'You win!')
        elif tic.game_win == 'AI':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
            bot.send_sticker(call.message.chat.id, tic.sti)
            bot.send_message(call.message.chat.id, f'You lose!')
        elif tic.game_win == 'Draw':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
            bot.send_sticker(call.message.chat.id, tic.sti)
            bot.send_message(call.message.chat.id, f'Ok, draw!')
        elif tic.game_win == ' ':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=tic,
                                  reply_markup=tic.keyboard)


bot.polling(none_stop=True)
