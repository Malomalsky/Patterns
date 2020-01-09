#-*- encoding: utf-8 -*-
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional
from cli import *

class Handler(ABC):
    """
    Интерфейс Обработчика объявляет метод построения цепочки обработчиков. Он
    также объявляет метод для выполнения запроса.
    """

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    """
    Поведение цепочки по умолчанию может быть реализовано внутри базового класса
    обработчика.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        # Возврат обработчика отсюда позволит связать обработчики простым
        # способом, вот так:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    @abstractmethod
    def handle(self, request: Any) -> str:
        if self._next_handler:
            return self._next_handler.handle(request)

        return None


"""
Все Конкретные Обработчики либо обрабатывают запрос, либо передают его
следующему обработчику в цепочке.
"""


class BagHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request in ('Кактус','Венерина Мухоловка'):
            return f"{request} доставляется самовывозом."
        else:
            return super().handle(request)


class CourierHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request in ('Пена для бритья','Журнал Игромания','Пицца Маргарита'):
            return f"{request} доставляется курьером."
        else:
            return super().handle(request)


    
class AirHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "Газонокосилка":
            return f"{request} доставляется авиапочтой."
        else:
            return super().handle(request)


def client_code(c, handler: Handler) -> None:
    """
    Обычно клиентский код приспособлен для работы с единственным обработчиком. В
    большинстве случаев клиенту даже неизвестно, что этот обработчик является
    частью цепочки.
    """

    for item in c:
        print(f"\nClient: Как доставляется {item}?")
        result = handler.handle(item)
        if result:
            print(f"  {result}", end="")
        else:
            print(f"В данном контексте доставка  {item} невозможна.", end="")


if __name__ == "__main__":
    bag = BagHandler()
    courier = CourierHandler()
    air= AirHandler()

    bag.set_next(courier).set_next(air)
    c = cli()
    # Клиент должен иметь возможность отправлять запрос любому обработчику, а не
    # только первому в цепочке.
    print("Chain: Самовывоз > Курьер > Авиапочта ")
    client_code(c, bag)
    print("\n")

    print("Subchain: Курьер > Авиапочта")
    client_code(c, courier)
