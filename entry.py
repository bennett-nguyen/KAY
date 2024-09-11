from sys import exit

import pygame as pg

from src.window import pygame_window
from src.utils import const
from src.main.app import App

app = App()
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

    app.process_input(events)
    app.update_view(dt_time)

    pg.display.update()
