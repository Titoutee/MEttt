from pygame import *

class Button:
    __slots__ = 'rect', 'clickable'
    def __init__(self, rect):
        self.rect = rect
        self.clickable = True
    
    def add_image(self, img, window):
        window.blit(img, self.rect)

    def is_clickable(self):
        return self.clickable
    
def clicked_on_who(m_x, m_y, buttons):
    assert isinstance(m_x, int) and isinstance(m_y, int)
    for r, row in enumerate(buttons):
        for c, button in enumerate(row):
            assert isinstance(button.rect, Rect)
            if button.rect.collidepoint(m_x, m_y):
                return r, c