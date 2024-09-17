import flet as ft
class Play(ft.Container):
    def __init__(self, size):
        super().__init__(self)
        self._size = size
        self.space = 10
        self.height = self._size + (self.space*2)
        self.width  = self._size + (self.space*2)
        self.bgcolor = ft.colors.BLACK