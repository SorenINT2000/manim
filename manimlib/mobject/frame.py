from __future__ import annotations

from manimlib.constants import BLACK, GREY_E
from manimlib.constants import FRAME_HEIGHT
from manimlib.mobject.geometry import Rectangle

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from manimlib.typing import ManimColor


class ScreenRectangle(Rectangle):
    """
    A rectangle that has the same aspect ratio as the screen.

    This class is used to create a rectangle that has the same aspect ratio
    as the screen.

    Parameters
    ----------
    aspect_ratio
        The aspect ratio of the rectangle.
    height
        The height of the rectangle.
    """
    def __init__(
        self,
        aspect_ratio: float = 16.0 / 9.0,
        height: float = 4,
        **kwargs
    ):
        super().__init__(
            width=aspect_ratio * height,
            height=height,
            **kwargs
        )


class FullScreenRectangle(ScreenRectangle):
    """
    A screen rectangle that fills the entire screen.

    This class is used to create a screen rectangle that fills the entire
    screen.

    Parameters
    ----------
    height
        The height of the rectangle.
    fill_color
        The fill color of the rectangle.
    fill_opacity
        The fill opacity of the rectangle.
    stroke_width
        The stroke width of the rectangle.
    """
    def __init__(
        self,
        height: float = FRAME_HEIGHT,
        fill_color: ManimColor = GREY_E,
        fill_opacity: float = 1,
        stroke_width: float = 0,
        **kwargs,
    ):
        super().__init__(
            height=height,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            stroke_width=stroke_width,
            **kwargs
        )


class FullScreenFadeRectangle(FullScreenRectangle):
    """
    A full screen rectangle that is used to fade the screen.

    This class is used to create a full screen rectangle that is used to fade
    the screen.

    Parameters
    ----------
    stroke_width
        The stroke width of the rectangle.
    fill_color
        The fill color of the rectangle.
    fill_opacity
        The fill opacity of the rectangle.
    """
    def __init__(
        self,
        stroke_width: float = 0.0,
        fill_color: ManimColor = BLACK,
        fill_opacity: float = 0.7,
        **kwargs,
    ):
        super().__init__(
            stroke_width=stroke_width,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
        )
