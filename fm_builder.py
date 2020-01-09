from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
from typing import Any
import time
import sqlite3
import random
import smtplib
from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
from email.mime.text import MIMEText                # Текст/HTML
import ssl

# ---------------------------------------------Фабричный метод--------------------------------------------------------
class Creator(ABC):
    """
    Класс Создатель объявляет фабричный метод, который должен возвращать объект
    класса Продукт. 
    """
    @abstractmethod
    def factory_method(self):
        pass

    def some_operation(self) -> str:
        # Вызываем фабричный метод, чтобы получить объект-продукт.
        product = self.factory_method()
        # Далее, работаем с этим продуктом.
        result = f"Creator: Создан объект класса  {product.name}"
        return result


"""
Конкретные Создатели переопределяют фабричный метод для того, чтобы изменить тип
результирующего продукта.
"""


class ShipCreator(Creator):
    def factory_method(self) -> Ship:
        """Данный метод создает объект класса Корабль, записывает информацию в базу данных и после немного спит."""
        conn = sqlite3.connect("db.sqlite")
        cursor = conn.cursor()
        info = ('Ship', str(datetime.now()))
        cursor.execute("INSERT INTO logs VALUES (?,?)", info)
        conn.commit()
        time.sleep(random.randint(0,2))
        return Ship()

class TruckCreator(Creator):
    def factory_method(self) -> Truck:
        """Данный метод создает объект класса Грузовик, записывает информацию в базу данных и после немного спит."""
        conn = sqlite3.connect("db.sqlite")
        cursor = conn.cursor()
        info = ('Truck', str(datetime.now()))
        cursor.execute("INSERT INTO logs VALUES (?,?)", info)
        conn.commit()
        time.sleep(random.randint(0,2))
        return Truck()


class Product(ABC):
    """
    Интерфейс Продукта объявляет операции, которые должны выполнять все
    конкретные продукты.
    """

    @abstractmethod
    def operation(self) -> str:
        pass

"""
Конкретные Продукты предоставляют различные реализации интерфейса Продукта.
"""

class Ship(Product):
    def __init__(self):
        self.name = 'Корабль'
    def operation(self) -> str:
        return "Корабль"

class Truck(Product):
    def __init__(self):
        self.name = 'Грузовик'
    def operation(self) -> str:
        return "Грузовик"


def client_code(creator: Creator) -> None:
    """
    Клиентский код работает с экземпляром конкретного создателя, хотя и через
    его базовый интерфейс. Пока клиент продолжает работать с создателем через
    базовый интерфейс, вы можете передать ему любой подкласс создателя.
    """

    print(f"Client: Меня не волнует класс Создателя, я работаю.\n"
          f"{creator.some_operation()}", end="")

#----------------------------------------Билдер---------------------------------------------------------
class Builder(ABC):
    """
    Интерфейс Строителя объявляет создающие методы для различных частей объектов
    Продуктов.
    """

    @abstractproperty
    def product(self) -> None:
        pass

    @abstractmethod
    def produce_part_a(self) -> None:
        pass

    @abstractmethod
    def produce_part_b(self) -> None:
        pass

    @abstractmethod
    def produce_part_c(self) -> None:
        pass

class ConcreteBuilder1(Builder):
    """
    Классы Конкретного Строителя следуют интерфейсу Строителя и предоставляют
    конкретные реализации шагов построения.
    """

    def __init__(self) -> None:
        """
        Новый экземпляр строителя должен содержать пустой объект продукта,
        который используется в дальнейшей сборке.
        """
        self.reset()
        
    def reset(self) -> None:
        self._product = Product1()

    @property
    def product(self) -> Product1:
        product = self._product
        self.reset()
        return product

    def produce_part_a(self) -> None:
        """
        В данном методе мы задаем техническую информацию - адресата, получателя 
        """
        self._product.add("Техническая информация")
        addr_from = "testpatternsmgupi@gmail.com"                # Адресат
        addr_to   = "lores78518@xmail2.net"                      # Получатель                              
        self._product.msg['From'] = addr_from
        self._product.msg['To']   = addr_to                      # Получатель
        self._product.msg['Subject'] = 'Отчет'                   # Тема сообщения


    def produce_part_b(self) -> None:
        """В данном методе происходит построение тела письма"""
        conn = sqlite3.connect("db.sqlite")
        conn1 = sqlite3.connect("db.sqlite")
        curs = conn.cursor()
        curs1 = conn1.cursor()
        sql_truck = "SELECT COUNT(*) FROM logs WHERE name = 'Truck'"
        curs.execute(sql_truck)
        TruckCount = curs.fetchone()[0]
        conn.close()
        print(TruckCount)
        sql_ship = "SELECT COUNT(*) FROM logs WHERE name = 'Ship'" 
        curs1.execute(sql_ship)
        ShipCount = curs1.fetchone()[0]
        conn1.close()
        print(ShipCount)
        body  = f"На данный момент произведено {TruckCount} грузовиков и {ShipCount} кораблей"
        if TruckCount > ShipCount:
            body += "\n Нужно строить больше ангаров!"
        elif ShipCount > TruckCount:
            body += "\n Нужно строить больше верфей"
        else:
            pass
        self._product.add("Тело письма")
        self._product.msg.attach(MIMEText(body, 'plain'))
    def produce_part_c(self) -> None:
        self._product.add("PartC1")


class Product1():

    def __init__(self) -> None:
        self.parts = []
        self.msg = MIMEMultipart()
       

    def add(self, part: Any) -> None:
        self.parts.append(part)

    def send_mes(self) -> None:
        password  = 'iv27ko98'
        addr_from = "testpatternsmgupi@gmail.com"                 # Адресат
        context = ssl.create_default_context()
        server = smtplib.SMTP('smtp.gmail.com', 587)          # Создаем объект SMTP
        server.ehlo()
        #server.set_debuglevel(True)                         # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
        server.starttls(context=context)                                   # Начинаем шифрованный обмен по TLS
        server.ehlo()
        server.login(addr_from, password)                   # Получаем доступ
        server.send_message(self.msg)                            # Отправляем сообщение
        server.quit()   
        print('Сообщение отправлено')                    

class Director:
    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:

        self._builder = builder

    def build_minimal_viable_product(self) -> None:
        self.builder.produce_part_a()
        self.builder.produce_part_b

    def build_full_featured_product(self) -> None:
        self.builder.produce_part_a()
        self.builder.produce_part_b()
        self.builder.produce_part_c()




#-----------------------------------------------Тест--------------------------------------------------
if __name__ == "__main__":
    n = 0
    while n != 100:
        if n%30 == 0:
            builder = ConcreteBuilder1()
            builder.produce_part_a()
            builder.produce_part_b()
            builder.product.send_mes()

        ran = random.randint(1,2)
        if ran == 1:
            print("App: Запущено с  ShipCreator.")
            client_code(ShipCreator())
            print("\n"+"*"*140)
            n += 1
        else:
            print("App: Запущено с  TruckCreator.")
            client_code(TruckCreator())
            print("\n"+"*"*140)
            n+=1
    print("App: генерация завершена")
