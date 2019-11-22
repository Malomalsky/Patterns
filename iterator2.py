#-*- encoding: utf-8 -*-


class CountTo:
    def __init__(self, upperBound):
        self.upperBound = upperBound
        self.numbersInEnglish = ["one", "two", "three", "four", "five", 'six', 'seven', 'eight', 'nine']
        self.numbersInEnglish = self.numbersInEnglish[:upperBound]              
        self.index = 0                                                          # Нужен для отслеживания текущей позиции итератора в списке
    def __iter__(self):
        return self
    def __next__(self):
        try:
            result = self.numbersInEnglish[self.index]
        except IndexError:
            print('В итерируемой структуре данных объектов меньше, чем введенное число')
            raise StopIteration
            
        self.index += 1
        return result
 
c = int(input('Введите количество обьектов (1-9)'))

countToN = CountTo(c)
for i in range(countToN.upperBound):
    print(next(countToN))

