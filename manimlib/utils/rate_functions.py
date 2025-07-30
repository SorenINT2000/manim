from __future__ import annotations

import numpy as np

from manimlib.utils.bezier import bezier

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable


def linear(t: float) -> float:
    """A linear rate function."""
    return t


def smooth(t: float) -> float:
    """A smooth rate function."""
    # Zero first and second derivatives at t=0 and t=1.
    # Equivalent to bezier([0, 0, 0, 1, 1, 1])
    s = 1 - t
    return (t**3) * (10 * s * s + 5 * s * t + t * t)


def rush_into(t: float) -> float:
    """A rate function that rushes into the animation."""
    return 2 * smooth(0.5 * t)


def rush_from(t: float) -> float:
    """A rate function that rushes from the animation."""
    return 2 * smooth(0.5 * (t + 1)) - 1


def slow_into(t: float) -> float:
    """A rate function that slows into the animation."""
    return np.sqrt(1 - (1 - t) * (1 - t))


def double_smooth(t: float) -> float:
    """A rate function that is smooth on both ends."""
    if t < 0.5:
        return 0.5 * smooth(2 * t)
    else:
        return 0.5 * (1 + smooth(2 * t - 1))


def there_and_back(t: float) -> float:
    """A rate function that goes there and back."""
    new_t = 2 * t if t < 0.5 else 2 * (1 - t)
    return smooth(new_t)


def there_and_back_with_pause(t: float, pause_ratio: float = 1. / 3) -> float:
    """A rate function that goes there and back with a pause in the middle."""
    a = 2. / (1. - pause_ratio)
    if t < 0.5 - pause_ratio / 2:
        return smooth(a * t)
    elif t < 0.5 + pause_ratio / 2:
        return 1
    else:
        return smooth(a - a * t)


def running_start(t: float, pull_factor: float = -0.5) -> float:
    """A rate function that has a running start."""
    return bezier([0, 0, pull_factor, pull_factor, 1, 1, 1])(t)


def overshoot(t: float, pull_factor: float = 1.5) -> float:
    """A rate function that overshoots the end."""
    return bezier([0, 0, pull_factor, pull_factor, 1, 1])(t)


def not_quite_there(
    func: Callable[[float], float] = smooth,
    proportion: float = 0.7
) -> Callable[[float], float]:
    """A rate function that doesn't quite get to the end."""
    def result(t):
        return proportion * func(t)
    return result


def wiggle(t: float, wiggles: float = 2) -> float:
    """A rate function that wiggles."""
    return there_and_back(t) * np.sin(wiggles * np.pi * t)


def squish_rate_func(
    func: Callable[[float], float],
    a: float = 0.4,
    b: float = 0.6
) -> Callable[[float], float]:
    """A rate function that squishes another rate function."""
    def result(t):
        if a == b:
            return a
        elif t < a:
            return func(0)
        elif t > b:
            return func(1)
        else:
            return func((t - a) / (b - a))

    return result

# Stylistically, should this take parameters (with default values)?
# Ultimately, the functionality is entirely subsumed by squish_rate_func,
# but it may be useful to have a nice name for with nice default params for
# "lingering", different from squish_rate_func's default params


def lingering(t: float) -> float:
    """A rate function that lingers at the end."""
    return squish_rate_func(lambda t: t, 0, 0.8)(t)


def exponential_decay(t: float, half_life: float = 0.1) -> float:
    """An exponential decay rate function."""
    # The half-life should be rather small to minimize
    # the cut-off error at the end
    return 1 - np.exp(-t / half_life)
