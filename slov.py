import random


def Slowo():
    a = random.randint(1, 532)
    while a % 2 == 0:
        a = random.randint(1, 532)
    with open('eng.txt', 'r', encoding="utf8") as file:
        my_list = []
        i = 0
        for item in file:
            i += 1
            if i == a:
                my_list.append(item)
                return f'{my_list[0]}'
