def clicked_on(x, y, width, height, m_x, m_y):
    return x<=m_x<=x+width and y<=m_y<=height

def clicked_on_who(m_x, m_y, buttons: list):
    for idx, button in enumerate(buttons):
        if button.collidepoint(m_x, m_y):
            yield idx