class Employee:
    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary
    
    def display_info(self):
        return self.name, self.age, self.salary

obj1 = Employee('Kanishk', 22, 200000)
print(obj1.display_info())