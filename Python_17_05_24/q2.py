class Shape:
    def area(self):
        pass

class circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * (self.radius ** 2)

class rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return int(self.width * self.height)
    
    def area(self):
        return float(self.width * self.height)

class triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

obj1 = circle(5)
obj2 = rectangle(4.2, 6.0)
obj3 = triangle(3, 7)

print(obj1.area())
print(obj2.area())
print(obj3.area())


