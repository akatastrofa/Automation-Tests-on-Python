"""CREATE FILE figures_data

class Rectangle:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def getArea(self):
        return self.a * self.b

class Square:
    def __init__(self, a):
        self.a = a

    def getAreaSq(self):
        return self.a ** 2

import math

class Circle:
        def __init__(self, r):
        self.r = r

    def getAreaCrcl(self):
        return math.pi * (self.r ** 2)

    def getAreaCrcl2(self):
        return math.pi / 4 * ((self.r + self.r) ** 2)
        
        
"""CREATE FILE get_some_figures"""

from figures_data import Rectangle, Square, Circle

rect_1 = Rectangle(3, 4)
rect_2 = Rectangle(12, 5)

sq_1 = Square(2)
sq_2 = Square(5)

cr_1 = Circle(2)
cr_2 = Circle(6)

figures = [rect_1, rect_2, sq_1, sq_2, cr_1, cr_2]
for figure in figures:
    if isinstance(figure, Square):
        print('Квадратова площадь: ', figure.getAreaSq())
    elif isinstance(figure, Circle):
        print('Кругова площадь: ', figure.getAreaCrcl() or figure.getAreaCrcl2())
    else:
        print('Прямоугольникова площадь: ', figure.getArea())
