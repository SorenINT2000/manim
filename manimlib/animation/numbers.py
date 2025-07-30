from __future__ import annotations

from manimlib.animation.animation import Animation
from manimlib.mobject.numbers import DecimalNumber
from manimlib.utils.bezier import interpolate
from manimlib.utils.simple_functions import clip

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable


class ChangingDecimal(Animation):
    """
    Animates the changing of a decimal number.

    This animation shows a decimal number changing its value over time,
    according to a specified update function.

    Parameters
    ----------
    decimal_mob
        The decimal number to be animated.
    number_update_func
        The function that updates the value of the decimal number.
    suspend_mobject_updating
        A boolean indicating whether the mobject's updaters should be
        suspended during the animation.
    """
    def __init__(
        self,
        decimal_mob: DecimalNumber,
        number_update_func: Callable[[float], float],
        suspend_mobject_updating: bool = False,
        **kwargs
    ):
        assert isinstance(decimal_mob, DecimalNumber)
        self.number_update_func = number_update_func
        super().__init__(
            decimal_mob,
            suspend_mobject_updating=suspend_mobject_updating,
            **kwargs
        )
        self.mobject = decimal_mob

    def interpolate_mobject(self, alpha: float) -> None:
        true_alpha = self.time_spanned_alpha(alpha)
        new_value = self.number_update_func(true_alpha)
        self.mobject.set_value(new_value)


class ChangeDecimalToValue(ChangingDecimal):
    """
    Animates the changing of a decimal number to a specific value.

    This animation is a specialization of `ChangingDecimal` that changes the
    value of a decimal number to a specified target value.

    Parameters
    ----------
    decimal_mob
        The decimal number to be animated.
    target_number
        The target value of the decimal number.
    """
    def __init__(
        self,
        decimal_mob: DecimalNumber,
        target_number: float | complex,
        **kwargs
    ):
        start_number = decimal_mob.number
        super().__init__(
            decimal_mob,
            lambda a: interpolate(start_number, target_number, a),
            **kwargs
        )


class CountInFrom(ChangingDecimal):
    """
    Animates the counting in of a decimal number from a source value.

    This animation is a specialization of `ChangingDecimal` that shows a
    decimal number counting in from a specified source value.

    Parameters
    ----------
    decimal_mob
        The decimal number to be animated.
    source_number
        The source value of the decimal number.
    """
    def __init__(
        self,
        decimal_mob: DecimalNumber,
        source_number: float | complex = 0,
        **kwargs
    ):
        start_number = decimal_mob.get_value()
        super().__init__(
            decimal_mob,
            lambda a: interpolate(source_number, start_number, clip(a, 0, 1)),
            **kwargs
        )
