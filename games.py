from random import randint
from telebot import types


class GameSpoke:
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
        self.items = ('\U0001F91C', '\U0000270C', '\U0001FAF3', '\U0001F90F', '\U0001F596')
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
            self.sti = open('game_win.webp', 'rb')
        elif self.player_health == 0:
            self.game_win = 'AI'
            self.sti = open('game_lose.webp', 'rb')

    def __str__(self):
        if self.player_move == '':
            return f'Камень, ножницы, бумага, ящерица, Спок\nс Шелдоном Купером!\n\n\U0001F466  \U00002694  \U0001F468\U0000200D\U0001F4BB\n\n\U0001F468\U0000200D\U0001F4BB Шелдон\n\U00002764 {self.ai_health}/5\n\n\U0001F466 {self.player_name}\n\U00002764 {self.player_health}/5\n'
        else:
            return f'Камень, ножницы, бумага, ящерица, Спок\nc Шелдоном Купером!\n\n\U0001F466  \U00002694  \U0001F468\U0000200D\U0001F4BB\n\n\U0001F468\U0000200D\U0001F4BB Шелдон\n\U00002764 {self.ai_health}/5\nПоходил:  {self.ai_move}\n\n\U0001F466 {self.player_name}\n\U00002764 {self.player_health}/5\nПоходил:  {self.player_move}'


class GameTicTacToe:
    # X = \U0000274C
    # O = \U00002B55

    def __init__(self, game_win=' ', sti=''):
        self.field = [[" "] * 3 for _ in range(3)]
        self.game_win = game_win
        self.win_cord = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                         ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                         ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))

        self.items = ('0 0', '0 1', '0 2', '1 0', '1 1', '1 2', '2 0', '2 1', '2 2')
        self.keyboard = types.InlineKeyboardMarkup(row_width=3)
        self.but1 = types.InlineKeyboardButton(game_win, callback_data='0 0')
        self.but2 = types.InlineKeyboardButton(game_win, callback_data='0 1')
        self.but3 = types.InlineKeyboardButton(game_win, callback_data='0 2')
        self.but4 = types.InlineKeyboardButton(game_win, callback_data='1 0')
        self.but5 = types.InlineKeyboardButton(game_win, callback_data='1 1')
        self.but6 = types.InlineKeyboardButton(game_win, callback_data='1 2')
        self.but7 = types.InlineKeyboardButton(game_win, callback_data='2 0')
        self.but8 = types.InlineKeyboardButton(game_win, callback_data='2 1')
        self.but9 = types.InlineKeyboardButton(game_win, callback_data='2 2')
        self.keyboard.add(self.but1, self.but2, self.but3, self.but4, self.but5, self.but6, self.but7, self.but8,
                          self.but9)
        self.sti = sti

    def move(self, player_move):
        def change_buttons(name, smile):
            if name == '0 0':
                self.but1 = types.InlineKeyboardButton(f"{smile}", callback_data='---')
            elif name == '0 1':
                self.but2 = types.InlineKeyboardButton(f"{smile}", callback_data='---')
            elif name == '0 2':
                self.but3 = types.InlineKeyboardButton(f"{smile}", callback_data='---')
            elif name == '1 0':
                self.but4 = types.InlineKeyboardButton(f"{smile}", callback_data='---')
            elif name == '1 1':
                self.but5 = types.InlineKeyboardButton(f"{smile}", callback_data='---')
            elif name == '1 2':
                self.but6 = types.InlineKeyboardButton(f"{smile}", callback_data='---')
            elif name == '2 0':
                self.but7 = types.InlineKeyboardButton(f"{smile}", callback_data='---')
            elif name == '2 1':
                self.but8 = types.InlineKeyboardButton(f"{smile}", callback_data='---')
            elif name == '2 2':
                self.but9 = types.InlineKeyboardButton(f"{smile}", callback_data='---')
            self.keyboard = types.InlineKeyboardMarkup(row_width=3)
            self.keyboard.add(self.but1, self.but2, self.but3, self.but4, self.but5, self.but6, self.but7, self.but8,
                              self.but9)

        def check_win():
            for cord in self.win_cord:
                symbols = []
                for c in cord:
                    symbols.append(self.field[c[0]][c[1]])
                if symbols == ["X", "X", "X"]:
                    self.game_win = 'Player'
                    self.sti = open('game_win.webp', 'rb')
                elif " " not in [a for b in self.field for a in b] and self.game_win != 'Player':
                    self.game_win = 'Draw'
                    self.sti = open('game_draw.webp', 'rb')
                if symbols == ["O", "O", "O"]:
                    self.game_win = 'AI'
                    self.sti = open('game_lose.webp', 'rb')

        self.field[int(player_move[0])][int(player_move[-1])] = "X"
        change_buttons(player_move, '\U0000274C')
        check_win()

        if " " in [a for b in self.field for a in b]:
            while True:
                x = randint(0, 2)
                y = randint(0, 2)
                if self.field[x][y] == " ":
                    self.field[x][y] = "O"
                    change_buttons(f'{x} {y}', '\U00002B55')
                    check_win()
                    break

    def __str__(self):
        return 'Крестики-Нолики\nс Шелдоном Купером!'
