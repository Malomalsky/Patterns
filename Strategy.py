from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Context():
    """
    Контекст определяет интерфейс, представляющий интерес для клиентов.
    """

    def __init__(self, strategy: Strategy) -> None:
        """
        Обычно Контекст принимает стратегию через конструктор, а также
        предоставляет сеттер для её изменения во время выполнения.
        """

        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        """
        Контекст хранит ссылку на один из объектов Стратегии. Контекст не знает
        конкретного класса стратегии. Он должен работать со всеми стратегиями
        через интерфейс Стратегии.
        """

        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        """
        Обычно Контекст позволяет заменить объект Стратегии во время выполнения.
        """

        self._strategy = strategy

    def do_some_business_logic(self) -> None:
        """
        Вместо того, чтобы самостоятельно реализовывать множественные версии
        алгоритма, Контекст делегирует некоторую работу объекту Стратегии.
        """

        # ...
        try:
            print("Context: Sorting data using the strategy  \n")

            result = self._strategy.do_algorithm(nums)
            print(",".join(result))
        except TypeError:
            pass
        # ...


class Strategy(ABC):
    """
    Интерфейс Стратегии объявляет операции, общие для всех поддерживаемых версий
    некоторого алгоритма.

    Контекст использует этот интерфейс для вызова алгоритма, определённого
    Конкретными Стратегиями.
    """

    @abstractmethod
    def do_algorithm(self, data: List):
        pass


"""
Конкретные Стратегии реализуют алгоритм, следуя базовому интерфейсу Стратегии.
Этот интерфейс делает их взаимозаменяемыми в Контексте.
"""


class ConcreteStrategyA(Strategy):
    def do_algorithm(self, data: List) -> List:
        return sorted(data)


class ConcreteStrategyB(Strategy):
    def do_algorithm(self, data: List) -> List:
        return reversed(sorted(data))

class ConcreteStrategyC(Strategy):
    def do_algorithm(self, data: List) -> List:
    # Устанавливаем swapped в True, чтобы цикл запустился хотя бы один раз
        k = 1
        swapped = True
        while swapped:
            swapped = False
            for i in range(len(nums) - 1):
                print("Итерация {0}, список - {1}".format(k, nums))
                k += 1
                if nums[i] > nums[i + 1]:
                    # Меняем элементы
                    nums[i], nums[i + 1] = nums[i + 1], nums[i]
                    # Устанавливаем swapped в True для следующей итерации
                    swapped = True
        return nums
                    

if __name__ == "__main__":
    # Клиентский код выбирает конкретную стратегию и передаёт её в контекст.
    # Клиент должен знать о различиях между стратегиями, чтобы сделать
    # правильный выбор.

    while True:
        nums =[]
        print("Вводите цифры для сортировки по одной, а если захотите выйти, введите Exit: ")
        while True:
            num = input()
            if num != 'Exit':
                nums.append(num)
            elif num == 'Exit':
                break
        break

    context = Context(ConcreteStrategyA())
    print("Client: Strategy is set to normal sorting.")
    context.do_some_business_logic()
    print()

    print("Client: Strategy is set to reverse sorting.")
    context.strategy = ConcreteStrategyB()
    context.do_some_business_logic()
    
    
    print("Client: Strategy is set to reverse sorting.")
    context.strategy = ConcreteStrategyC()
    context.do_some_business_logic()