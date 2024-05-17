class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
    
    def display_info(self):
        return self.make, self.model, self.year

obj1 = Car('Mahindra', 'xuv500', 2016)
print(obj1.display_info())


