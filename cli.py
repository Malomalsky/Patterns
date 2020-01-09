#-*- encoding: utf-8 -*-
from os import system
import pprint
from pyfiglet import Figlet


f = Figlet(font='slant')
print(f.renderText('Shop'))

def cli():
    """Интерфейс магазина: каталог и корзина."""
    catalog = {1:'Кактус',2:'Венерина Мухоловка', 3:'Пена для бритья',4:'Газонокосилка', 5:'Пицца Маргарита', 6:'Журнал Игромания'}
    f = Figlet(font='slant')
    print(f.renderText('Shop'))
    corz = []
    while True:
        print('Добро пожаловать в каталог магазина! Для добавления товара в корзину введите номер товара,  для выхода и совершения оплаты нажмите 7.\n')
        for i in catalog:
            print(f"{i}.{catalog[i]}")
        str_cors = ','.join(corz)
        print(f"Ваша корзина: {str_cors} \n")
        answer = int(input('Введите номер товара: '))
        if answer==7:
            break
        while True:
            try:
                system('clear')
                print(f"Добавить '{catalog[answer]}' в корзину? [Y/n]  \n") 
                ans2 = input()
                if ans2=='Y':
                    corz.append(catalog[answer])
                    system('clear')
                    break
                else:
                    break
            except KeyError:
                print("Введите правильное значение!")
    return corz



