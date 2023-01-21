import telebot
from telebot import types
from utils import get_news, Weather, Horoscope, Currency, Game
from config import tkn

bot = telebot.TeleBot(tkn)
weather = Weather()
horo = Horoscope()
cur = Currency()
battle = Game()


@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard_menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton('\U0001F326 Погода')
    button2 = types.KeyboardButton('\U0001F525 Новости')
    button3 = types.KeyboardButton('\U00002651 Гороскоп')
    button4 = types.KeyboardButton('\U0001F4B1 Конвертация валют')
    button5 = types.KeyboardButton('\U0001F3AE Миниигра')
    keyboard_menu.add(button1, button2, button3, button4, button5)
    sti = open('static\welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, f'Мяу, Мяу-Мяу, {message.chat.first_name}!', reply_markup=keyboard_menu)


@bot.message_handler(content_types=['text'])
def handle_weather(message):
    global weather, horo, cur, battle

    if message.chat.type == 'private':
        if message.text == '\U0001F326 Погода':
            bot.send_message(message.chat.id, f'Выберите ваш город:', reply_markup=weather.keyboard)
        elif message.text == '\U0001F525 Новости':
            bot.send_message(message.chat.id, f'\U0001F525 Лента новостей от "РБК":\n{get_news()}',
                             parse_mode='Markdown')
        elif message.text == '\U00002651 Гороскоп':
            bot.send_message(message.chat.id, f'Выберите свой знак зодиака:', reply_markup=horo.keyboard)
        elif message.text == '\U0001F4B1 Конвертация валют':
            bot.send_message(message.chat.id, f'Курсы валют:\n{cur.start_currency()}\nИз какой валюты переводим?',
                             reply_markup=cur.keyboard_from)
        elif message.text == '\U0001F3AE Миниигра':
            battle.sti = open('static\game_start.webp', 'rb')
            bot.send_sticker(message.chat.id, battle.sti)
            battle = Game(message.chat.first_name, '', 5, 5, '')
            bot.send_message(message.chat.id, battle, reply_markup=battle.keyboard)

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
    global weather, horo, cur, battle

    if call.data == 'Москва':
        bot.send_message(call.message.chat.id, weather.get_weather('Москва'))
    elif call.data == 'С.-Петербург':
        bot.send_message(call.message.chat.id, weather.get_weather('С.-Петербург'))
    elif call.data == 'Новосибирск':
        bot.send_message(call.message.chat.id, weather.get_weather('Новосибирск'))
    elif call.data == 'Екатеринбург':
        bot.send_message(call.message.chat.id, weather.get_weather('Екатеринбург'))
    elif call.data == 'Казань':
        bot.send_message(call.message.chat.id, weather.get_weather('Казань'))
    elif call.data == 'Н. Новгород':
        bot.send_message(call.message.chat.id, weather.get_weather('Н. Новгород'))
    elif call.data == 'Сочи':
        bot.send_message(call.message.chat.id, weather.get_weather('Сочи'))
    elif call.data == 'Самара':
        bot.send_message(call.message.chat.id, weather.get_weather('Самара'))
    elif call.data == 'aries':
        bot.send_message(call.message.chat.id, f'\U00002648 Овен:\n{horo.get_horo()[0]}')
    elif call.data == 'taurus':
        bot.send_message(call.message.chat.id, f'\U00002649 Телец:\n{horo.get_horo()[1]}')
    elif call.data == 'gemini':
        bot.send_message(call.message.chat.id, f'\U0000264A Близнецы:\n{horo.get_horo()[2]}')
    elif call.data == 'cancer':
        bot.send_message(call.message.chat.id, f'\U0000264B Рак:\n{horo.get_horo()[3]}')
    elif call.data == 'leo':
        bot.send_message(call.message.chat.id, f'\U0000264C Лев:\n{horo.get_horo()[4]}')
    elif call.data == 'virgo':
        bot.send_message(call.message.chat.id, f'\U0000264D Дева:\n{horo.get_horo()[5]}')
    elif call.data == 'libra':
        bot.send_message(call.message.chat.id, f'\U0000264E Весы:\n{horo.get_horo()[6]}')
    elif call.data == 'scorpio':
        bot.send_message(call.message.chat.id, f'\U0000264F Скорпион:\n{horo.get_horo()[7]}')
    elif call.data == 'sagittarius':
        bot.send_message(call.message.chat.id, f'\U00002650 Стрелец:\n{horo.get_horo()[8]}')
    elif call.data == 'capricorn':
        bot.send_message(call.message.chat.id, f'\U00002651 Козерог:\n{horo.get_horo()[9]}')
    elif call.data == 'aquarius':
        bot.send_message(call.message.chat.id, f'\U00002652 Водолей:\n{horo.get_horo()[10]}')
    elif call.data == 'pisces':
        bot.send_message(call.message.chat.id, f'\U00002653 Рыбы:\n{horo.get_horo()[11]}')
    elif call.data == 'from_RUB':
        cur.from_ = 'RUB'
        bot.send_message(call.message.chat.id, f'В какую валюту переводим?', reply_markup=cur.keyboard_to)
    elif call.data == 'from_USD':
        cur.from_ = 'USD'
        bot.send_message(call.message.chat.id, f'В какую валюту переводим?', reply_markup=cur.keyboard_to)
    elif call.data == 'from_EUR':
        cur.from_ = 'EUR'
        bot.send_message(call.message.chat.id, f'В какую валюту переводим?', reply_markup=cur.keyboard_to)
    elif call.data == 'from_СТН':
        cur.from_ = 'СТН'
        bot.send_message(call.message.chat.id, f'В какую валюту переводим?', reply_markup=cur.keyboard_to)
    elif call.data == 'from_JPY':
        cur.from_ = 'JPY'
        bot.send_message(call.message.chat.id, f'В какую валюту переводим?', reply_markup=cur.keyboard_to)
    elif call.data == 'from_KZT':
        cur.from_ = 'KZT'
        bot.send_message(call.message.chat.id, f'В какую валюту переводим?', reply_markup=cur.keyboard_to)
    elif call.data == 'from_GBP':
        cur.from_ = 'GBP'
        bot.send_message(call.message.chat.id, f'В какую валюту переводим?', reply_markup=cur.keyboard_to)
    elif call.data == 'from_BYN':
        cur.from_ = 'BYN'
        bot.send_message(call.message.chat.id, f'В какую валюту переводим?', reply_markup=cur.keyboard_to)
    elif call.data == 'from_GEL':
        cur.from_ = 'GEL'
        bot.send_message(call.message.chat.id, f'В какую валюту переводим?', reply_markup=cur.keyboard_to)
    elif call.data == 'to_RUB':
        cur.to_ = 'RUB'
        cur.currency_mode = True
        bot.send_message(call.message.chat.id, f'Введите сумму:')
    elif call.data == 'to_USD':
        cur.to_ = 'USD'
        cur.currency_mode = True
        bot.send_message(call.message.chat.id, f'Введите сумму:')
    elif call.data == 'to_EUR':
        cur.to_ = 'EUR'
        cur.currency_mode = True
        bot.send_message(call.message.chat.id, f'Введите сумму:')
    elif call.data == 'to_СТН':
        cur.to_ = 'СТН'
        cur.currency_mode = True
        bot.send_message(call.message.chat.id, f'Введите сумму:')
    elif call.data == 'to_JPY':
        cur.to_ = 'JPY'
        cur.currency_mode = True
        bot.send_message(call.message.chat.id, f'Введите сумму:')
    elif call.data == 'to_KZT':
        cur.to_ = 'KZT'
        cur.currency_mode = True
        bot.send_message(call.message.chat.id, f'Введите сумму:')
    elif call.data == 'to_GBP':
        cur.to_ = 'GBP'
        cur.currency_mode = True
        bot.send_message(call.message.chat.id, f'Введите сумму:')
    elif call.data == 'to_BYN':
        cur.to_ = 'BYN'
        cur.currency_mode = True
        bot.send_message(call.message.chat.id, f'Введите сумму:')
    elif call.data == 'to_GEL':
        cur.to_ = 'GEL'
        cur.currency_mode = True
        bot.send_message(call.message.chat.id, f'Введите сумму:')
    elif call.data == '\U0001F91C':
        battle.move('\U0001F91C')
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
    elif call.data == '\U0000270C':
        battle.move('\U0000270C')
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
    elif call.data == '\U0001FAF3':
        battle.move('\U0001FAF3')
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
    elif call.data == '\U0001F90F':
        battle.move('\U0001F90F')
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
    elif call.data == '\U0001F596':
        battle.move('\U0001F596')
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


bot.polling(none_stop=True)
