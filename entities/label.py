from services.config_loader import STAT_FONT, WIN_HEIGHT

class Label:
    
    COUNT = 0
    font = STAT_FONT
    
    def __init__(self, label, number=0):
        self.label = label
        self.number = number
        self.x = 50
        self.y = WIN_HEIGHT - (80 + Label.COUNT * 50)
        Label.COUNT += 1
        
    def set_number(self, number):
        self.number = number
    
    def increase(self, value=1):
        self.number += value
        
    def decrease(self, value=1):
        self.number -= value
        
    def reset(self):
        self.number = 0
        
    def get_render_object(self):
        return self.font.render(f"{self.label} : {self.number}", 1, (255,255,255))