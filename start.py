import telebot
from telebot import types
import datetime
import random
import moon
from anekdot import anecdot
import slov

import json

bot = telebot.TeleBot("Key")

# дни до нового года

#######


@bot.message_handler(commands=['start'])
def send_welcome(message):
    sey_hello = f'Привет, {message.from_user.first_name}\nВыберите действие:\n' \
                f'-Дни до Нового года? (нажмите или введите /ng) \n' \
                f'-Интересует фаза луны? (нажмите или введите /phase)\n' \
                f'-Хотите анекдот? (нажмите или введите /anecdot)\n'\
                f'-Случайное английское слово (нажмите или введите /slovo)\n'\
                f'-Поиграем в крестики нолики? (нажмите или введите /game)\n'
    bot.send_message(message.chat.id, sey_hello, parse_mode='html')


@bot.message_handler(commands=['ng'])
def send_welcome(message):
    date1 = datetime.date.today()
    date2 = datetime.date(2023, 12, 31)
    delta = date2 - date1
    days = str(delta).split(',')
    say = f'До нового года осталось {days[0]}'
    bot.send_message(message.chat.id, say, parse_mode='html')


@bot.message_handler(commands=['phase'])
def send_welcome(message):
    date_list = str(datetime.date.today()).split('-')
    day = int(date_list[2])
    month = int(date_list[1])
    MoonCh = 7
    say = moon.getPhaze(day, month, MoonCh)
    img = open(moon.Img(moon.getPhaze(day, month, MoonCh)), 'rb')
    bot.send_message(message.chat.id, say, parse_mode='html')
    bot.send_photo(message.chat.id, img)


@bot.message_handler(commands=['anecdot'])
def send_welcome(message):
    say = anecdot.message()
    bot.send_message(message.chat.id, say, parse_mode='html')


@bot.message_handler(commands=['slovo'])
def send_welcome(message):
    say = slov.Slowo()
    bot.send_message(message.chat.id, say, parse_mode='html')


@bot.message_handler(commands=['game'])
def send_xo(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    one_one = types.KeyboardButton('/r 0')
    one_two = types.KeyboardButton('/r 1')
    one_tree = types.KeyboardButton('/r 2')

    two_one = types.KeyboardButton('/r 3')
    two_two = types.KeyboardButton('/r 4')
    two_tree = types.KeyboardButton('/r 5')

    tree_one = types.KeyboardButton('/r 6')
    treee_two = types.KeyboardButton('/r 7')
    tree_tree = types.KeyboardButton('/r 8')
    markup.add(one_one, one_two, one_tree, two_one, two_two,
               two_tree, tree_one, treee_two, tree_tree)

    usid = message.from_user.id
    liste = ['..', '..', '..', '..', '..', '..',
             '..', '..', '..']  # исходный массив положений

    usname = message.from_user.first_name
    botname = "NAGIBATOR_BOT"
    New_user_obj(usid)
    say = f'| {liste[0]} | {liste[1]} | {liste[2]} |\n'\
          f'| {liste[3]} | {liste[4]} | {liste[5]} |\n'\
          f'| {liste[6]} | {liste[7]} | {liste[8]} |\n'\
          f'Выберите ячейку'
    bot.send_message(message.chat.id, say, reply_markup=markup)

    @bot.message_handler(commands=['r'])
    def play(message):
        Nolik = True
        while Nolik:
            str = message.text.split()

            hod = str[1]
            name = usname
            iter = 0
            Write(usid, hod, name)
            obj_hod = Read()[f'{usid}']["hodi"]
            obj_name = Read()[f'{usid}']["name"]
            for el in obj_hod:
                if obj_name[iter] == f'{name}':
                    liste[int(el)] = '0'
                else:
                    liste[int(el)] = 'X'
                iter += 1
            # заполнен массив истории ходов
            liste[int(hod)] = '0'

            say = f'| {liste[0]} | {liste[1]} | {liste[2]} |\n'\
                  f'| {liste[3]} | {liste[4]} | {liste[5]} |\n'\
                  f'| {liste[6]} | {liste[7]} | {liste[8]} |\n'\

            bot.send_message(message.chat.id, say, parse_mode='html')

            name = botname

            bothod = random.randint(0, 8)
            # проверка на заполненность
            while liste[int(bothod)] == '0' or liste[int(bothod)] == 'X':
                bothod = random.randint(0, 8)
            liste[int(bothod)] = 'X'

            Write(usid, bothod, name)

            say = f'| {liste[0]} | {liste[1]} | {liste[2]} |\n'\
                  f'| {liste[3]} | {liste[4]} | {liste[5]} |\n'\
                  f'| {liste[6]} | {liste[7]} | {liste[8]} |\n'\

            bot.send_message(message.chat.id, say, parse_mode='html')
            vin = False
            Proverka(liste, usid, usname, botname, message)
            if vin:
                break
            Nolik = False


def Read():
    with open('jso.json', 'r') as file:
        my_dict = json.load(file)
        return my_dict


def New_user_obj(id):
    my_dict = Read()
    flag = True

    for item in my_dict.keys():
        if item == f"{id}":
            flag = False

    if flag:
        my_dict.update({f"{id}": {}})
        my_dict[f'{id}'].update({"name": []})
        my_dict[f'{id}'].update({"hodi": []})

        with open('jso.json', 'w') as file:
            json.dump(my_dict, file, indent=4)


def Write(usid, hod: str, name: str):
    my_dict = Read()
    flag = True
    # with open("game.json", "w") as file:
    # my_dict = dict(json.load(file))

    for item in my_dict.keys():
        if item == f"{usid}":
            flag = False

    if flag:
        my_dict.update({f"{usid}": {}})
        my_dict[f'{usid}'].update({"name": [f"{name}"]})
        my_dict[f'{usid}'].update({"hodi": [f"{str(hod)}"]})
    else:
        my_dict[f'{usid}']["hodi"].append(str(hod))
        my_dict[f'{usid}']["name"].append(f'{name}')
    with open('jso.json', 'w') as file:
        json.dump(my_dict, file, indent=4)


def clear(id):
    my_dict = Read()
    my_dict[f'{id}']["hodi"] = []
    my_dict[f'{id}']["name"] = []
    with open('jso.js', 'w') as file:
        json.dump(my_dict, file, indent=4)


def Proverka(listik, usid, usname, botname, message):
    global vin
    if listik[0] == '0' and listik[1] == '0' and listik[2] == '0':
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        clear(usid)
        vin = False
        bot.send_message(
            message.chat.id, f'{usname} WIIIIN!!', parse_mode='html')

    if listik[3] == '0' and listik[4] == '0' and listik[5] == '0':
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        clear(usid)
        bot.send_message(
            message.chat.id, f'{usname} WIIIIN!!', parse_mode='html')
        vin = True

    if listik[6] == '0' and listik[7] == '0' and listik[8] == '0':
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        clear(usid)
        bot.send_message(
            message.chat.id, f'{usname} WIIIIN!!', parse_mode='html')
        vin = True

    if listik[0] == '0' and listik[4] == '0' and listik[8] == '0':
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        clear(usid)
        bot.send_message(
            message.chat.id, f'{usname} WIIIIN!!', parse_mode='html')
        vin = True

    if listik[2] == '0' and listik[4] == '0' and listik[6] == '0':
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        clear(usid)
        bot.send_message(
            message.chat.id, f'{usname} WIIIIN!!', parse_mode='html')
        vin = True

    if listik[0] == '0' and listik[3] == '0' and listik[6] == '0':
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        clear(usid)
        bot.send_message(
            message.chat.id, f'{usname} WIIIIN!!', parse_mode='html')
        vin = True

    if listik[1] == '0' and listik[4] == '0' and listik[7] == '0':
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        clear(usid)
        bot.send_message(
            message.chat.id, f'{usname} WIIIIN!!', parse_mode='html')
        vin = True

    if listik[2] == '0' and listik[5] == '0' and listik[8] == '0':
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        clear(usid)
        bot.send_message(
            message.chat.id, f'{usname} WIIIIN!!', parse_mode='html')
        vin = True

    if listik[0] == 'X' and listik[1] == 'X' and listik[2] == 'X':
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        clear(usid)
        bot.send_message(message.chat.id, F'{botname} WINN', parse_mode='html')
        vin = True

    if listik[3] == 'X' and listik[4] == 'X' and listik[5] == 'X':
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        clear(usid)
        bot.send_message(message.chat.id, F'{botname} WINN', parse_mode='html')
        vin = True

    if listik[6] == 'X' and listik[7] == 'X' and listik[8] == 'X':
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        clear(usid)
        bot.send_message(message.chat.id, F'{botname} WINN', parse_mode='html')
        vin = True

    if listik[0] == 'X' and listik[4] == 'X' and listik[8] == 'X':
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        clear(usid)
        bot.send_message(message.chat.id, F'{botname} WINN', parse_mode='html')
        vin = True

    if listik[2] == 'X' and listik[4] == 'X' and listik[6] == 'X':
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        clear(usid)
        bot.send_message(message.chat.id, F'{botname} WINN', parse_mode='html')
        vin = True

    if listik[0] == 'X' and listik[3] == 'X' and listik[6] == 'X':
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        bot.send_message(message.chat.id, F'{botname} WINN', parse_mode='html')
        print(f'X winner')
        vin = True

    if listik[1] == 'X' and listik[4] == 'X' and listik[7] == 'X':
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        clear(usid)
        bot.send_message(message.chat.id, F'{botname} WINN', parse_mode='html')
        vin = True

    if listik[2] == 'X' and listik[5] == 'X' and listik[8] == 'X':
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        clear(usid)
        bot.send_message(message.chat.id, F'{botname} WINN', parse_mode='html')
        vin = True

    if listik.count('..') == 0:
        listik = ['..', '..', '..', '..', '..', '..', '..', '..', '..']
        clear(usid)
        bot.send_message(message.chat.id, F'НИЧЬЯ', parse_mode='html')
        vin = True


bot.infinity_polling()
