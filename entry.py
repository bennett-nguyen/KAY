from sys import exit

import pygame as pg

from src.core import pygame_window
from src.core.utils import const
from src.mvc.controller import Controller

controller = Controller()
model = controller.model

theme_manager = model.theme_manager
focus_gained: bool = True

while True:
    events = pg.event.get()

    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

        if event.type == pg.WINDOWFOCUSLOST:
            focus_gained = False
        elif event.type == pg.WINDOWFOCUSGAINED:
            focus_gained = True

    if focus_gained:
        dt_time = pygame_window.set_framerate(const.ACTIVE_FPS) / 1000.0
    else:
        dt_time = pygame_window.set_framerate(const.IDLE_FPS) / 1000.0

    controller.process_input(events)
    controller.update_view(dt_time)

    pg.display.update()
