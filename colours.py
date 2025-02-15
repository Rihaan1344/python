class Colour:
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.orange = (255, 165, 0)
    
    def get_colour(self, colour):
        return getattr(self, colour, (255, 255, 255))