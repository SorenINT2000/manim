from __future__ import annotations

from functools import lru_cache
import hashlib
import inspect
import math

import numpy as np

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable, TypeVar, Iterable
    from manimlib.typing import FloatArray

    Scalable = TypeVar("Scalable", float, FloatArray)



def sigmoid(x: float | FloatArray):
    """
    Sigmoid function.
    """
    return 1.0 / (1 + np.exp(-x))


@lru_cache(maxsize=10)
def choose(n: int, k: int) -> int:
    """
    Computes n choose k.
    """
    return math.comb(n, k)


def gen_choose(n: int, r: int) -> int:
    """
    Computes n choose r.
    """
    return int(np.prod(range(n, n - r, -1)) / math.factorial(r))


def get_num_args(function: Callable) -> int:
    """
    Returns the number of arguments of a function.
    """
    return function.__code__.co_argcount


def get_parameters(function: Callable) -> Iterable[str]:
    """
    Returns the parameters of a function.
    """
    return inspect.signature(function).parameters.keys()


def clip(a: float, min_a: float, max_a: float) -> float:
    """
    Clips a value to a given range.
    """
    if a < min_a:
        return min_a
    elif a > max_a:
        return max_a
    return a


def arr_clip(arr: np.ndarray, min_a: float, max_a: float) -> np.ndarray:
    """
    Clips an array to a given range.
    """
    arr[arr < min_a] = min_a
    arr[arr > max_a] = max_a
    return arr


def fdiv(a: Scalable, b: Scalable, zero_over_zero_value: Scalable | None = None) -> Scalable:
    """
    Less heavyweight name for np.true_divide, enabling
    default behavior for 0/0
    """
    if zero_over_zero_value is not None:
        out = np.full_like(a, zero_over_zero_value)
        where = np.logical_or(a != 0, b != 0)
    else:
        out = None
        where = True

    return np.true_divide(a, b, out=out, where=where)


def binary_search(
    function: Callable[[float], float],
    target: float,
    lower_bound: float,
    upper_bound: float,
    tolerance:float = 1e-4
) -> float | None:
    """
    Performs a binary search to find the input to a function that gives a certain target value.
    """
    lh = lower_bound
    rh = upper_bound
    mh = (lh + rh) / 2
    while abs(rh - lh) > tolerance:
        lx, mx, rx = [function(h) for h in (lh, mh, rh)]
        if lx == target:
            return lx
        if rx == target:
            return rx

        if lx <= target and rx >= target:
            if mx > target:
                rh = mh
            else:
                lh = mh
        elif lx > target and rx < target:
            lh, rh = rh, lh
        else:
            return None
        mh = (lh + rh) / 2
    return mh


def hash_string(string: str, n_bytes=16) -> str:
    """
    Returns a hash of a string.
    """
    hasher = hashlib.sha256(string.encode())
    return hasher.hexdigest()[:n_bytes]
