class Shapes:
    def circle(self, rad, area):
        self.area = 3.14*(self.rad)**2
        return self.area

    def rectangle(self, l, b, area):
        self.area = l*b
        return self.area
    
    def square(self,side,area):
        self.area = side**2
        return self.area

    def triangle(self, b, h, area):
        self.area = 0.5*b*h
        return self.area
    

