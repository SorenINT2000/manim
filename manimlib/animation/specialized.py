from __future__ import annotations

from manimlib.animation.composition import LaggedStart
from manimlib.animation.transform import Restore
from manimlib.constants import BLACK, WHITE
from manimlib.mobject.geometry import Circle
from manimlib.mobject.types.vectorized_mobject import VGroup

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
    from manimlib.typing import ManimColor


class Broadcast(LaggedStart):
    """
    Animates a broadcast effect.

    This animation shows a series of concentric circles emanating from a
    focal point, creating a "broadcast" effect.

    Parameters
    ----------
    focal_point
        The point from which the broadcast emanates.
    small_radius
        The radius of the smallest circle.
    big_radius
        The radius of the largest circle.
    n_circles
        The number of circles in the broadcast.
    start_stroke_width
        The stroke width of the smallest circle.
    color
        The color of the circles.
    run_time
        The duration of the animation.
    lag_ratio
        The time lag between the start of each circle's animation.
    remover
        A boolean indicating whether the circles should be removed from the
        scene after the animation is complete.
    """
    def __init__(
        self,
        focal_point: np.ndarray,
        small_radius: float = 0.0,
        big_radius: float = 5.0,
        n_circles: int = 5,
        start_stroke_width: float = 8.0,
        color: ManimColor = WHITE,
        run_time: float = 3.0,
        lag_ratio: float = 0.2,
        remover: bool = True,
        **kwargs
    ):
        self.focal_point = focal_point
        self.small_radius = small_radius
        self.big_radius = big_radius
        self.n_circles = n_circles
        self.start_stroke_width = start_stroke_width
        self.color = color

        circles = VGroup()
        for x in range(n_circles):
            circle = Circle(
                radius=big_radius,
                stroke_color=BLACK,
                stroke_width=0,
            )
            circle.add_updater(lambda c: c.move_to(focal_point))
            circle.save_state()
            circle.set_width(small_radius * 2)
            circle.set_stroke(color, start_stroke_width)
            circles.add(circle)
        super().__init__(
            *map(Restore, circles),
            run_time=run_time,
            lag_ratio=lag_ratio,
            remover=remover,
            **kwargs
        )
