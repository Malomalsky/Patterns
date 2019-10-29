
# -*- coding: utf-8 -*-
from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List


class Subject(ABC):
    """
    Интферфейс издателя объявляет набор методов для управлениями подпискичами.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Присоединяет наблюдателя к издателю.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Отсоединяет наблюдателя от издателя.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Уведомляет всех наблюдателей о событии.
        """
        pass


class ConcreteSubject(Subject):
    """
    Издатель владеет некоторым важным состоянием и оповещает наблюдателей о его
    изменениях.
    """

    _state: int = None
    """
    в этой переменной хранится состояние Издателя, необходимое всем подписчикам.
    """

    _observers: List[Observer] = []
    """
    Список подписчиков. 
    """

    def attach(self, observer: Observer) -> None:
        print("Subject: Прикреплен наблюдатель.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if len(self._observers) > 0:
            print("Subject: Откреплен наблюдатель.")
            self._observers.remove(observer)

    """
    Методы управления подпиской.
    """

    def notify(self) -> None:
        """
        Запуск обновления в каждом подписчике.
        """

        print("Subject: Уведомляю наблюдателей...")
        for observer in self._observers:
            observer.update(self)

    def some_business_logic(self) -> None:

        print("\nSubject: Делаю кое-что важное.")
        self._state = randrange(0, 1000)

        print(f"Subject: Цена подписки изменена на: {self._state}")
        self.notify()


class Observer(ABC):
    """
    Интерфейс Наблюдателя объявляет метод уведомления, который издатели
    используют для оповещения своих подписчиков.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Получить обновление от субъекта.
        """
        pass


"""
Конкретные Наблюдатели реагируют на обновления, выпущенные Издателем, к которому
они прикреплены.
"""


class ConcreteObserverA(Observer):
    def update(self, subject: Subject) -> None:
        if subject._state > 300:
            print("Наблюдатель А: Реагирую на событие. \n Я отменяю подписку.")


class ConcreteObserverB(Observer):
    def update(self, subject: Subject) -> None:
        if subject._state == 0 or subject._state >= 400:
            print("Наблюдатель Б: Реагирую на событие. \n Я отменяю подписку.")


if __name__ == "__main__":
    # Клиентский код.

    subject = ConcreteSubject()

    observer_a = ConcreteObserverA()
    subject.attach(observer_a)

    observer_b = ConcreteObserverB()
    subject.attach(observer_b)
    try:
        subject.some_business_logic()
        if subject._state > 300:
            subject.detach(observer_a)
        if subject._state >= 400:
            subject.detach(observer_b)
        subject.some_business_logic()
        if subject._state > 300:
            subject.detach(observer_a)
        if subject._state >= 400:
            subject.detach(observer_b)


        subject.some_business_logic()
        if subject._state > 300:
            subject.detach(observer_a)
        if subject._state >= 400:
            subject.detach(observer_b)
    except ValueError:
        print("Подписчиков не осталось")