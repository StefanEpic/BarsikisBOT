import requests
from bs4 import BeautifulSoup
import feedparser
import datetime
from random import randint
from telebot import types
from config import tkn_w, tkn_c


class Weather:
    def __init__(self):
        self.dic_city = {
            'Москва': 'Moscow',
            'С.-Петербург': 'Saint Petersburg',
            'Новосибирск': 'Novosibirsk',
            'Екатеринбург': 'Yekaterinburg',
            'Казань': 'Kazan',
            'Н. Новгород': 'Nizhny Novgorod',
            'Сочи': 'Sochi',
            'Самара': 'Samara'
        }

        self.keyboard = types.InlineKeyboardMarkup(row_width=2)
        but1 = types.InlineKeyboardButton("Москва", callback_data='Москва')
        but2 = types.InlineKeyboardButton("С.-Петербург", callback_data='С.-Петербург')
        but3 = types.InlineKeyboardButton("Новосибирск", callback_data='Новосибирск')
        but4 = types.InlineKeyboardButton("Екатеринбург", callback_data='Екатеринбург')
        but5 = types.InlineKeyboardButton("Казань", callback_data='Казань')
        but6 = types.InlineKeyboardButton("Н. Новгород", callback_data='Н. Новгород')
        but7 = types.InlineKeyboardButton("Сочи", callback_data='Сочи')
        but8 = types.InlineKeyboardButton("Самара", callback_data='Самара')
        self.keyboard.add(but1, but2, but3, but4, but5, but6, but7, but8)

    def get_weather(self, city):
        w = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={self.dic_city[city]}&appid={tkn_w}&units=metric').json()
        weather_smile = {
            'Thunderstorm': 'Гроза \U000026C8',
            'Drizzle': 'Морось \U0001F328',
            'Rain': 'Дождь \U0001F327',
            'Snow': 'Снег \U0001F328',
            'Mist': 'Туман \U0001F32B',
            'Smoke': 'Дымка \U0001F32B',
            'Haze': 'Мгла \U0001F32B',
            'Fog': 'Туман \U0001F32B',
            'Squall': 'Шквал \U0001F4A8',
            'Clear': 'Ясно \U00002600',
            'Clouds': 'Облачно \U00002601'
        }

        if w['weather'][0]['main'] in weather_smile:
            weather_smile = weather_smile[w['weather'][0]['main']]
        else:
            weather_smile = ''

        weather = [
            f"Погода в городе {city} на {datetime.date.today().strftime('%d:%m:%Y')}:\n",
            f"\U0001F321 Температура: {round(w['main']['temp'])} °C, {weather_smile}\n",
            f"\U0001F321 Ощущается как: {round(w['main']['feels_like'])} °C\n",
            f"\U00002600 Днем: {round(w['main']['temp_max'])} °C\n",
            f"\U0001F319 Ночью: {round(w['main']['temp_min'])} °C\n",
            f"\U0001F4A7 Влажность: {w['main']['humidity']}%\n",
            f"\U0001F449 Давление: {w['main']['pressure']} мм.рт.ст\n",
            f"\U0001F4A8 Скорость ветра: {round(w['wind']['speed'])} м/с\n",
            f"Восход: {str(datetime.datetime.fromtimestamp(w['sys']['sunrise']))[11:]}\n",
            f"Закат: {str(datetime.datetime.fromtimestamp(w['sys']['sunset']))[11:]}\n",
            f"Продолжительность дня: {datetime.datetime.fromtimestamp(w['sys']['sunset']) - datetime.datetime.fromtimestamp(w['sys']['sunrise'])}\n"
        ]
        return ''.join(weather)


def get_news():
    feed = feedparser.parse('http://static.feed.rbc.ru/rbc/logical/footer/news.rss')
    news = ''.join([f'{_ + 1}. [{entry.title}]({entry.link})\n' for _, entry in enumerate(feed.entries[:10])])
    return news


class Horoscope:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup(row_width=3)
        but1 = types.InlineKeyboardButton("\U00002648 Овен", callback_data='aries')
        but2 = types.InlineKeyboardButton("\U00002649 Телец", callback_data='taurus')
        but3 = types.InlineKeyboardButton("\U0000264A Близнецы", callback_data='gemini')
        but4 = types.InlineKeyboardButton("\U0000264B Рак", callback_data='cancer')
        but5 = types.InlineKeyboardButton("\U0000264C Лев", callback_data='leo')
        but6 = types.InlineKeyboardButton("\U0000264D Дева", callback_data='virgo')
        but7 = types.InlineKeyboardButton("\U0000264E Весы", callback_data='libra')
        but8 = types.InlineKeyboardButton("\U0000264F Скорпион", callback_data='scorpio')
        but9 = types.InlineKeyboardButton("\U00002650 Стрелец", callback_data='sagittarius')
        but10 = types.InlineKeyboardButton("\U00002651 Козерог", callback_data='capricorn')
        but11 = types.InlineKeyboardButton("\U00002652 Водолей", callback_data='aquarius')
        but12 = types.InlineKeyboardButton("\U00002653 Рыбы", callback_data='pisces')
        self.keyboard.add(but1, but2, but3, but4, but5, but6, but7, but8,
                          but9, but10, but11, but12)

    @staticmethod
    def get_horo():
        feed = BeautifulSoup(requests.get('https://ignio.com/r/export/utf/xml/daily/com.xml').text, 'xml')
        feed = feed.find_all('today')
        horo = [_.text.replace('\n', '') for _ in feed]
        return horo


class Currency:
    def __init__(self, from_='', to_='', currency_mode=False):
        self.from_ = from_
        self.to_ = to_
        self.currency_mode = currency_mode

        self.keyboard_from = types.InlineKeyboardMarkup(row_width=3)
        from_but1 = types.InlineKeyboardButton("RUB", callback_data='from_RUB')
        from_but2 = types.InlineKeyboardButton("USD", callback_data='from_USD')
        from_but3 = types.InlineKeyboardButton("EUR", callback_data='from_EUR')
        from_but4 = types.InlineKeyboardButton("СТН", callback_data='from_СТН')
        from_but5 = types.InlineKeyboardButton("JPY", callback_data='from_JPY')
        from_but6 = types.InlineKeyboardButton("KZT", callback_data='from_KZT')
        from_but7 = types.InlineKeyboardButton("GBP", callback_data='from_GBP')
        from_but8 = types.InlineKeyboardButton("BYN", callback_data='from_BYN')
        from_but9 = types.InlineKeyboardButton("GEL", callback_data='from_GEL')
        self.keyboard_from.add(from_but1, from_but2, from_but3, from_but4, from_but5,
                               from_but6, from_but7, from_but8, from_but9)

        self.keyboard_to = types.InlineKeyboardMarkup(row_width=3)
        to_but1 = types.InlineKeyboardButton("RUB", callback_data='to_RUB')
        to_but2 = types.InlineKeyboardButton("USD", callback_data='to_USD')
        to_but3 = types.InlineKeyboardButton("EUR", callback_data='to_EUR')
        to_but4 = types.InlineKeyboardButton("СТН", callback_data='to_СТН')
        to_but5 = types.InlineKeyboardButton("JPY", callback_data='to_JPY')
        to_but6 = types.InlineKeyboardButton("KZT", callback_data='to_KZT')
        to_but7 = types.InlineKeyboardButton("GBP", callback_data='to_GBP')
        to_but8 = types.InlineKeyboardButton("BYN", callback_data='to_BYN')
        to_but9 = types.InlineKeyboardButton("GEL", callback_data='to_GEL')
        self.keyboard_to.add(to_but1, to_but2, to_but3, to_but4, to_but5, to_but6,
                             to_but7, to_but8, to_but9)

    @staticmethod
    def start_currency():
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=1"
        usd = requests.request("GET", url, headers={"apikey": tkn_c}, data={})
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=EUR&amount=1"
        eur = requests.request("GET", url, headers={"apikey": tkn_c}, data={})
        return f"USD = {round(usd.json()['info']['rate'], 2)} руб.\nEUR = {round(eur.json()['info']['rate'], 2)} руб.\n"

    def get_currency(self, amount=1):
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={self.to_}&from={self.from_}&amount={amount}"
        currency = requests.request("GET", url, headers={"apikey": tkn_c}, data={})
        return f"{amount} {self.from_} = {round(amount * currency.json()['info']['rate'], 2)} {self.to_}"


class Game:
    # stone = \U0001F91C
    # scissors = \U0000270C
    # paper = \U0001FAF3
    # lizard = \U0001F90F
    # spoke = \U0001F596

    def __init__(self, player_name='', player_move='', player_health=5, ai_health=5, game_win='', sti=''):
        self.player_name = player_name
        self.player_move = player_move
        self.player_health = player_health
        self.ai_health = ai_health
        self.ai_move = ''
        self.items = ['\U0001F91C', '\U0000270C', '\U0001FAF3', '\U0001F90F', '\U0001F596']
        self.game_win = game_win

        self.keyboard = types.InlineKeyboardMarkup(row_width=5)
        but1 = types.InlineKeyboardButton("\U0001F91C", callback_data='\U0001F91C')
        but2 = types.InlineKeyboardButton("\U0000270C", callback_data='\U0000270C')
        but3 = types.InlineKeyboardButton("\U0001FAF3", callback_data='\U0001FAF3')
        but4 = types.InlineKeyboardButton("\U0001F90F", callback_data='\U0001F90F')
        but5 = types.InlineKeyboardButton("\U0001F596", callback_data='\U0001F596')
        self.keyboard.add(but1, but2, but3, but4, but5)

        self.sti = sti

    def move(self, player_move):
        self.ai_move = self.items[randint(0, 4)]
        self.player_move = player_move
        if player_move == self.ai_move:
            pass
        elif player_move == '\U0001F91C' and (self.ai_move == '\U0000270C' or self.ai_move == '\U0001F90F'):
            self.ai_health -= 1
        elif player_move == '\U0000270C' and (self.ai_move == '\U0001FAF3' or self.ai_move == '\U0001F90F'):
            self.ai_health -= 1
        elif player_move == '\U0001FAF3' and (self.ai_move == '\U0001F91C' or self.ai_move == '\U0001F596'):
            self.ai_health -= 1
        elif player_move == '\U0001F90F' and (self.ai_move == '\U0001F596' or self.ai_move == '\U0001FAF3'):
            self.ai_health -= 1
        elif player_move == '\U0001F596' and (self.ai_move == '\U0001F91C' or self.ai_move == '\U0000270C'):
            self.ai_health -= 1
        else:
            self.player_health -= 1

        if self.ai_health == 0:
            self.game_win = 'Player'
            self.sti = open('static\game_win.webp', 'rb')
        elif self.player_health == 0:
            self.game_win = 'AI'
            self.sti = open('static\game_lose.webp', 'rb')

    def __str__(self):
        if self.player_move == '':
            return f'Камень, ножницы, бумага, ящерица, Спок\nс Шелдном Купером!\n\n\U0001F466  \U00002694  \U0001F468\U0000200D\U0001F4BB\n\n\U0001F468\U0000200D\U0001F4BB Шелдон\n\U00002764 {self.ai_health}/5\n\n\U0001F466 {self.player_name}\n\U00002764 {self.player_health}/5\n'
        else:
            return f'Камень, ножницы, бумага, ящерица, Спок\nc Шелдном Купером!\n\n\U0001F466  \U00002694  \U0001F468\U0000200D\U0001F4BB\n\n\U0001F468\U0000200D\U0001F4BB Шелдон\n\U00002764 {self.ai_health}/5\nПоходил:  {self.ai_move}\n\n\U0001F466 {self.player_name}\n\U00002764 {self.player_health}/5\nПоходил:  {self.player_move}'
