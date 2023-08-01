import pygame as pg

class Theme:
    def __init__(self, palette_obj):
        __slots__ = (
            "BACKGROUND_CLR",
            "NODE_FILLINGS_CLR",
            "NODE_OUTLINE_CLR",
            "LINE_CLR"
        )

        self.BACKGROUND_CLR: pg.Color = pg.Color(*palette_obj["background"])
        self.NODE_FILLINGS_CLR: pg.Color = pg.Color(*palette_obj["node_fillings"])
        self.NODE_OUTLINE_CLR: pg.Color = pg.Color(*palette_obj["node_outline"])

        self.LINE_CLR: pg.Color = pg.Color(*palette_obj["line"])