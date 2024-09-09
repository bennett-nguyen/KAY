import pygame as pg

from pygame.locals import *

from src.core.utils import const

pg.init()
pg.event.set_allowed(
    [
        QUIT,
        KEYDOWN,
        KEYUP,
        MOUSEBUTTONDOWN,
        MOUSEBUTTONUP,
        MOUSEMOTION,
        WINDOWFOCUSGAINED,
        WINDOWFOCUSLOST
    ]
)

class PygameWindow:
    __slots__ = ("screen", "clock")
    def __init__(self):
        info_obj = pg.display.Info()

        WIDTH: int = int(info_obj.current_w * const.DEFAULT_SCREEN_OCCUPATION_PERCENTAGE)
        HEIGHT: int = int(info_obj.current_h * const.DEFAULT_SCREEN_OCCUPATION_PERCENTAGE)

        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
        self.clock = pg.time.Clock()

        icon = pg.image.load("./icon/icon.ico").convert_alpha()
        pg.display.set_caption(f"Segment Tree Visualizer v{const.VERSION}")
        pg.display.set_icon(icon)

    def fill_background(self, color: pg.Color):
        self.screen.fill(color)

    def set_framerate(self, FPS: float) -> float:
        return self.clock.tick(FPS)

    @property
    def size(self) -> tuple[int, int]:
        return self.screen.get_size()

    @property
    def window_width(self) -> int:
        return self.screen.get_width()

    @property
    def window_height(self) -> int:
        return self.screen.get_height()
    
    @property
    def half_window_width(self) -> int:
        return int(self.window_width / 2)

    @property
    def half_window_height(self) -> int:
        return int(self.window_height / 2)

pygame_window = PygameWindow()