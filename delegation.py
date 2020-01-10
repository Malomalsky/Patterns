#coding: utf-8
#python 3
class A:
    def f(self):
        print('A : вызываем метод f')
    def g(self):
        print('A : вызываем метод g')
class C:
    def __init__(self):
        self.A = A()
    def f(self):
        return self.A.f()
    def g(self):
        return self.A.g()
c = C()
c.f() #A: вызываем метод f
c.g() #A: вызываем метод g