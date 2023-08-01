import pygame as pg

class Theme:
    def __init__(self, palette_obj):
        __slots__ = (
            "BACKGROUND_CLR",
            "NODE_FILLINGS_CLR",
            "NODE_OUTLINE_CLR",
            "NODE_DISPLAY_DATA_CLR"
            "LINE_CLR",
            "NODE_DISPLAY_DATA_HIGHLIGHT",
            "NODE_OUTLINE_HIGHLIGHT"
        )

        # Background
        self.BACKGROUND_CLR: pg.Color = pg.Color(*palette_obj["background"])

        # Node
        self.NODE_FILLINGS_CLR: pg.Color = pg.Color(*palette_obj["node_fillings"])
        self.NODE_OUTLINE_CLR: pg.Color = pg.Color(*palette_obj["node_outline"])
        self.NODE_DISPLAY_DATA_CLR: pg.Color = pg.Color(*palette_obj["node_display_data"])

        self.NODE_OUTLINE_HIGHLIGHT_CLR: pg.Color = pg.Color(*palette_obj["node_outline_highlight"])
        self.NODE_DISPLAY_DATA_HIGHLIGHT_CLR: pg.Color = pg.Color(*palette_obj["node_display_data_highlight"])

        # Line
        self.LINE_CLR: pg.Color = pg.Color(*palette_obj["line"])
