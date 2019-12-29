import pygame
class Main_Menu(pygame.Surface):
    def __init__(self,parent_window):
        super().__init__(parent_window.get_size())
        self.parent=parent_window
