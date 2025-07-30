from __future__ import annotations

from manimlib.animation.transform import Transform

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np

    from manimlib.mobject.geometry import Arrow
    from manimlib.mobject.mobject import Mobject
    from manimlib.typing import ManimColor


class GrowFromPoint(Transform):
    """
    Animates the growing of a mobject from a point.

    This animation shows the mobject growing from a specified point, as if it
    were being created from that point.

    Parameters
    ----------
    mobject
        The mobject to be grown.
    point
        The point to grow the mobject from.
    point_color
        The color of the point.
    """
    def __init__(
        self,
        mobject: Mobject,
        point: np.ndarray,
        point_color: ManimColor = None,
        **kwargs
    ):
        self.point = point
        self.point_color = point_color
        super().__init__(mobject, **kwargs)

    def create_target(self) -> Mobject:
        return self.mobject.copy()

    def create_starting_mobject(self) -> Mobject:
        start = super().create_starting_mobject()
        start.scale(0)
        start.move_to(self.point)
        if self.point_color is not None:
            start.set_color(self.point_color)
        return start


class GrowFromCenter(GrowFromPoint):
    """
    Animates the growing of a mobject from its center.

    This animation is a specialization of `GrowFromPoint` that grows the
    mobject from its center.

    Parameters
    ----------
    mobject
        The mobject to be grown.
    """
    def __init__(self, mobject: Mobject, **kwargs):
        point = mobject.get_center()
        super().__init__(mobject, point, **kwargs)


class GrowFromEdge(GrowFromPoint):
    """
    Animates the growing of a mobject from one of its edges.

    This animation is a specialization of `GrowFromPoint` that grows the
    mobject from a specified edge.

    Parameters
    ----------
    mobject
        The mobject to be grown.
    edge
        The edge to grow the mobject from.
    """
    def __init__(self, mobject: Mobject, edge: np.ndarray, **kwargs):
        point = mobject.get_bounding_box_point(edge)
        super().__init__(mobject, point, **kwargs)


class GrowArrow(GrowFromPoint):
    """
    Animates the growing of an arrow.

    This animation is a specialization of `GrowFromPoint` that grows an
    arrow from its start point.

    Parameters
    ----------
    arrow
        The arrow to be grown.
    """
    def __init__(self, arrow: Arrow, **kwargs):
        point = arrow.get_start()
        super().__init__(arrow, point, **kwargs)
