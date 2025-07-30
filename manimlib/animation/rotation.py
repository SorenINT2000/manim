from __future__ import annotations

from manimlib.animation.animation import Animation
from manimlib.constants import ORIGIN, OUT
from manimlib.constants import PI, TAU
from manimlib.utils.rate_functions import linear
from manimlib.utils.rate_functions import smooth

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
    from typing import Callable
    from manimlib.mobject.mobject import Mobject


class Rotating(Animation):
    """
    Animates the rotation of a mobject.

    This animation shows a mobject rotating by a specified angle about a
    specified axis.

    Parameters
    ----------
    mobject
        The mobject to be rotated.
    angle
        The angle of rotation.
    axis
        The axis of rotation.
    about_point
        The point about which to rotate the mobject.
    about_edge
        The edge about which to rotate the mobject.
    run_time
        The duration of the animation.
    rate_func
        The rate function to use for the animation.
    suspend_mobject_updating
        A boolean indicating whether the mobject's updaters should be
        suspended during the animation.
    """
    def __init__(
        self,
        mobject: Mobject,
        angle: float = TAU,
        axis: np.ndarray = OUT,
        about_point: np.ndarray | None = None,
        about_edge: np.ndarray | None = None,
        run_time: float = 5.0,
        rate_func: Callable[[float], float] = linear,
        suspend_mobject_updating: bool = False,
        **kwargs
    ):
        self.angle = angle
        self.axis = axis
        self.about_point = about_point
        self.about_edge = about_edge
        super().__init__(
            mobject,
            run_time=run_time,
            rate_func=rate_func,
            suspend_mobject_updating=suspend_mobject_updating,
            **kwargs
        )

    def interpolate_mobject(self, alpha: float) -> None:
        pairs = zip(
            self.mobject.family_members_with_points(),
            self.starting_mobject.family_members_with_points(),
        )
        for sm1, sm2 in pairs:
            for key in sm1.pointlike_data_keys:
                sm1.data[key][:] = sm2.data[key]
        self.mobject.rotate(
            self.rate_func(self.time_spanned_alpha(alpha)) * self.angle,
            axis=self.axis,
            about_point=self.about_point,
            about_edge=self.about_edge,
        )


class Rotate(Rotating):
    """
    Animates the rotation of a mobject by a specific angle.

    This animation is a specialization of `Rotating` that rotates a mobject
    by a specified angle.

    Parameters
    ----------
    mobject
        The mobject to be rotated.
    angle
        The angle of rotation.
    axis
        The axis of rotation.
    run_time
        The duration of the animation.
    rate_func
        The rate function to use for the animation.
    about_edge
        The edge about which to rotate the mobject.
    """
    def __init__(
        self,
        mobject: Mobject,
        angle: float = PI,
        axis: np.ndarray = OUT,
        run_time: float = 1,
        rate_func: Callable[[float], float] = smooth,
        about_edge: np.ndarray = ORIGIN,
        **kwargs
    ):
        super().__init__(
            mobject, angle, axis,
            run_time=run_time,
            rate_func=rate_func,
            about_edge=about_edge,
            **kwargs
        )
