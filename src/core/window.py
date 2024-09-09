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
    """
    Represents a window for the Pygame application, managing the display and 
    rendering settings. This class initializes the window, sets the icon and caption, 
    and provides methods to manipulate the window's appearance and frame rate.
    """

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
        """
        Fills the window's background with the specified color. 
        This method is used to clear the screen before drawing new graphics, ensuring 
        that the previous frame does not interfere with the current one.

        Args:
            color (pg.Color): The color to fill the background with.
        """

        self.screen.fill(color)

    def set_framerate(self, FPS: float) -> float:
        """
        Sets the frame rate for the application and regulates the speed of the game loop. 

        Args:
            FPS (float): The desired frames per second for the application.
        """

        return self.clock.tick(FPS)

    @property
    def size(self) -> tuple[int, int]:
        """
        Retrieves the current size of the window. 
        This property returns the width and height of the window as a tuple, allowing 
        other components of the application to adapt to the window's dimensions.

        Returns:
            tuple[int, int]: A tuple containing the width and height of the window.
        """

        return self.screen.get_size()

    @property
    def window_width(self) -> int:
        """
        Retrieves the current width of the window. 

        Returns:
            int: The width of the window in pixels.
        """

        return self.screen.get_width()

    @property
    def window_height(self) -> int:
        """
        Retrieves the current height of the window. 

        Returns:
            int: The height of the window in pixels.
        """

        return self.screen.get_height()
    
    @property
    def half_window_width(self) -> int:
        """
        Retrieves half the current width of the window. 

        Returns:
            int: Half the width of the window in pixels.
        """

        return int(self.window_width / 2)

    @property
    def half_window_height(self) -> int:
        """
        Retrieves half the current height of the window. 

        Returns:
            int: Half the height of the window in pixels.
        """

        return int(self.window_height / 2)

pygame_window = PygameWindow()