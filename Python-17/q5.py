class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    
    def display_info(self):
        return self.title, self.author, self.pages

obj1 = Book('Goosebumps', 'RL-Stine', 150)
print(obj1.display_info())