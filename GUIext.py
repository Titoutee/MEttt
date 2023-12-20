from pygame import *

class Button:
    __slots__ = 'rect'
    def __init__(self, rect):
        self.rect = rect
    
    def add_image(self, img, window):
        window.blit(img, self.rect)

def clicked_on_who(m_x, m_y, buttons: list):
    for idx, button in enumerate(buttons):
        if button.collidepoint(m_x, m_y):
            yield idx