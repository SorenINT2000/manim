from __future__ import annotations

from manimlib.animation.animation import Animation

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable

    from manimlib.mobject.mobject import Mobject


class UpdateFromFunc(Animation):
    """
    Animates a mobject by applying an update function to it.

    This animation applies a function to a mobject at each frame of the
    animation. This is useful when the state of one mobject is dependent
    on another simultaneously animated mobject.

    Parameters
    ----------
    mobject
        The mobject to be animated.
    update_function
        The function to be applied to the mobject at each frame.
    suspend_mobject_updating
        A boolean indicating whether the mobject's updaters should be
        suspended during the animation.
    """
    def __init__(
        self,
        mobject: Mobject,
        update_function: Callable[[Mobject], Mobject | None],
        suspend_mobject_updating: bool = False,
        **kwargs
    ):
        self.update_function = update_function
        super().__init__(
            mobject,
            suspend_mobject_updating=suspend_mobject_updating,
            **kwargs
        )

    def interpolate_mobject(self, alpha: float) -> None:
        self.update_function(self.mobject)


class UpdateFromAlphaFunc(Animation):
    """
    Animates a mobject by applying an update function that takes an alpha value.

    This animation applies a function to a mobject at each frame of the
    animation. The function takes the mobject and an alpha value as input,
    where the alpha value is the proportion of the animation that has been
    completed.

    Parameters
    ----------
    mobject
        The mobject to be animated.
    update_function
        The function to be applied to the mobject at each frame.
    suspend_mobject_updating
        A boolean indicating whether the mobject's updaters should be
        suspended during the animation.
    """
    def __init__(
        self,
        mobject: Mobject,
        update_function: Callable[[Mobject, float], Mobject | None],
        suspend_mobject_updating: bool = False,
        **kwargs
    ):
        self.update_function = update_function
        super().__init__(mobject, suspend_mobject_updating=suspend_mobject_updating, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        self.update_function(self.mobject, alpha)


class MaintainPositionRelativeTo(Animation):
    """
    Animates a mobject to maintain its position relative to another mobject.

    This animation keeps a mobject at a fixed position relative to another
    mobject, which may be moving.

    Parameters
    ----------
    mobject
        The mobject to be animated.
    tracked_mobject
        The mobject to which the animated mobject should maintain its
        position.
    """
    def __init__(
        self,
        mobject: Mobject,
        tracked_mobject: Mobject,
        **kwargs
    ):
        self.tracked_mobject = tracked_mobject
        self.diff = mobject.get_center() - tracked_mobject.get_center()
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        target = self.tracked_mobject.get_center()
        location = self.mobject.get_center()
        self.mobject.shift(target - location + self.diff)

class ApplyToUpdate(UpdateFromFunc):
    """
    Animates a mobject by applying a function to it and updating it.

    This animation is a specialization of `UpdateFromFunc` that applies a
    function to a mobject and then calls the mobject's `update` method.

    Parameters
    ----------
    mobject
        The mobject to be animated.
    func
        The function to be applied to the mobject at each frame.
    """
    def __init__(self, mobject: Mobject, func: Callable[[Mobject], None], **kwargs):
        super().__init__(mobject, func, **kwargs)
