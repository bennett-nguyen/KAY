import pygame as pg
import pygame_gui

from src.core.utils import const

class UIManager:
    def __init__(self):
        self.manager = pygame_gui.UIManager((const.WIDTH, const.HEIGHT), const.CMD_THEME_FILE)

    def update(self, dt_time: float):
        self.manager.update(dt_time)

    def process_event(self, event: pg.event.Event):
        self.manager.process_events(event)

    def draw(self, screen: pg.Surface):
        self.manager.draw_ui(screen)
