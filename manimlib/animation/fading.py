from __future__ import annotations

import numpy as np

from manimlib.animation.animation import Animation
from manimlib.animation.transform import Transform
from manimlib.constants import ORIGIN
from manimlib.mobject.types.vectorized_mobject import VMobject
from manimlib.mobject.mobject import Group
from manimlib.utils.bezier import interpolate
from manimlib.utils.rate_functions import there_and_back

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable
    from manimlib.mobject.mobject import Mobject
    from manimlib.scene.scene import Scene
    from manimlib.typing import Vect3


class Fade(Transform):
    """
    Abstract base class for fading animations.

    This class is not meant to be used directly, but rather to be subclassed
    by other fading animations.

    Parameters
    ----------
    mobject
        The mobject to be faded.
    shift
        The vector to shift the mobject by during the animation.
    scale
        The factor to scale the mobject by during the animation.
    """
    def __init__(
        self,
        mobject: Mobject,
        shift: np.ndarray = ORIGIN,
        scale: float = 1,
        **kwargs
    ):
        self.shift_vect = shift
        self.scale_factor = scale
        super().__init__(mobject, **kwargs)


class FadeIn(Fade):
    """
    Animates the fading in of a mobject.

    This animation fades the mobject in from a specified point, with a
    specified scale and shift.

    Parameters
    ----------
    mobject
        The mobject to be faded in.
    """
    def create_target(self) -> Mobject:
        return self.mobject.copy()

    def create_starting_mobject(self) -> Mobject:
        start = super().create_starting_mobject()
        start.set_opacity(0)
        start.scale(1.0 / self.scale_factor)
        start.shift(-self.shift_vect)
        return start


class FadeOut(Fade):
    """
    Animates the fading out of a mobject.

    This animation fades the mobject out to a specified point, with a
    specified scale and shift.

    Parameters
    ----------
    mobject
        The mobject to be faded out.
    remover
        A boolean indicating whether the mobject should be removed from the
        scene after the animation is complete.
    final_alpha_value
        The alpha value at which the animation finishes.
    """
    def __init__(
        self,
        mobject: Mobject,
        shift: Vect3 = ORIGIN,
        remover: bool = True,
        final_alpha_value: float = 0.0,  # Put it back in original state when done,
        **kwargs
    ):
        super().__init__(
            mobject, shift,
            remover=remover,
            final_alpha_value=final_alpha_value,
            **kwargs
        )

    def create_target(self) -> Mobject:
        result = self.mobject.copy()
        result.set_opacity(0)
        result.shift(self.shift_vect)
        result.scale(self.scale_factor)
        return result


class FadeInFromPoint(FadeIn):
    """
    Animates the fading in of a mobject from a point.

    This animation fades the mobject in from a specified point.

    Parameters
    ----------
    mobject
        The mobject to be faded in.
    point
        The point to fade the mobject in from.
    """
    def __init__(self, mobject: Mobject, point: Vect3, **kwargs):
        super().__init__(
            mobject,
            shift=mobject.get_center() - point,
            scale=np.inf,
            **kwargs,
        )


class FadeOutToPoint(FadeOut):
    """
fades the mobject out to a specified point.

    Parameters
    ----------
    mobject
        The mobject to be faded out.
    point
        The point to fade the mobject out to.
    """
    def __init__(self, mobject: Mobject, point: Vect3, **kwargs):
        super().__init__(
            mobject,
            shift=point - mobject.get_center(),
            scale=0,
            **kwargs,
        )


class FadeTransform(Transform):
    """
    Animates the transformation of a mobject into a target mobject, with a fading effect.

    This animation transforms the mobject into the target mobject, while
    fading the original mobject out and the target mobject in.

    Parameters
    ----------
    mobject
        The mobject to be transformed.
    target_mobject
        The target mobject of the transformation.
    stretch
        A boolean indicating whether the mobject should be stretched during
        the transformation.
    dim_to_match
        The dimension to match during the transformation.
    """
    def __init__(
        self,
        mobject: Mobject,
        target_mobject: Mobject,
        stretch: bool = True,
        dim_to_match: int = 1,
        **kwargs
    ):
        self.to_add_on_completion = target_mobject
        self.stretch = stretch
        self.dim_to_match = dim_to_match

        mobject.save_state()
        super().__init__(Group(mobject, target_mobject.copy()), **kwargs)

    def begin(self) -> None:
        self.ending_mobject = self.mobject.copy()
        Animation.begin(self)
        # Both 'start' and 'end' consists of the source and target mobjects.
        # At the start, the traget should be faded replacing the source,
        # and at the end it should be the other way around.
        start, end = self.starting_mobject, self.ending_mobject
        for m0, m1 in ((start[1], start[0]), (end[0], end[1])):
            self.ghost_to(m0, m1)

    def ghost_to(self, source: Mobject, target: Mobject) -> None:
        source.replace(target, stretch=self.stretch, dim_to_match=self.dim_to_match)
        source.set_uniform(**target.get_uniforms())
        source.set_opacity(0)

    def get_all_mobjects(self) -> list[Mobject]:
        return [
            self.mobject,
            self.starting_mobject,
            self.ending_mobject,
        ]

    def get_all_families_zipped(self) -> zip[tuple[Mobject]]:
        return Animation.get_all_families_zipped(self)

    def clean_up_from_scene(self, scene: Scene) -> None:
        Animation.clean_up_from_scene(self, scene)
        scene.remove(self.mobject)
        self.mobject[0].restore()
        if not self.remover:
            scene.add(self.to_add_on_completion)


class FadeTransformPieces(FadeTransform):
    """
    Animates the transformation of the pieces of a mobject into the pieces of a target mobject.

    This animation transforms the pieces of the mobject into the pieces of the
    target mobject, with a fading effect.

    Parameters
    ----------
    mobject
        The mobject to be transformed.
    target_mobject
        The target mobject of the transformation.
    """
    def begin(self) -> None:
        self.mobject[0].align_family(self.mobject[1])
        super().begin()

    def ghost_to(self, source: Mobject, target: Mobject) -> None:
        for sm0, sm1 in zip(source.get_family(), target.get_family()):
            super().ghost_to(sm0, sm1)


class VFadeIn(Animation):
    """
    VFadeIn and VFadeOut only work for VMobjects,
    """
    def __init__(self, vmobject: VMobject, suspend_mobject_updating: bool = False, **kwargs):
        super().__init__(
            vmobject,
            suspend_mobject_updating=suspend_mobject_updating,
            **kwargs
        )

    def interpolate_submobject(
        self,
        submob: VMobject,
        start: VMobject,
        alpha: float
    ) -> None:
        submob.set_stroke(
            opacity=interpolate(0, start.get_stroke_opacity(), alpha)
        )
        submob.set_fill(
            opacity=interpolate(0, start.get_fill_opacity(), alpha)
        )


class VFadeOut(VFadeIn):
    """
    Animates the fading out of a vectorized mobject.

    This animation is the reverse of `VFadeIn`, and it fades the vectorized
    mobject out of the screen.

    Parameters
    ----------
    vmobject
        The vectorized mobject to be faded out.
    remover
        A boolean indicating whether the mobject should be removed from the
        scene after the animation is complete.
    final_alpha_value
        The alpha value at which the animation finishes.
    """
    def __init__(
        self,
        vmobject: VMobject,
        remover: bool = True,
        final_alpha_value: float = 0.0,
        **kwargs
    ):
        super().__init__(
            vmobject,
            remover=remover,
            final_alpha_value=final_alpha_value,
            **kwargs
        )

    def interpolate_submobject(
        self,
        submob: VMobject,
        start: VMobject,
        alpha: float
    ) -> None:
        super().interpolate_submobject(submob, start, 1 - alpha)


class VFadeInThenOut(VFadeIn):
    """
    Animates the fading in and then out of a vectorized mobject.

    This animation fades the vectorized mobject in and then out of the
    screen.

    Parameters
    ----------
    vmobject
        The vectorized mobject to be faded in and out.
    rate_func
        The rate function to use for the animation.
    remover
        A boolean indicating whether the mobject should be removed from the
        scene after the animation is complete.
    final_alpha_value
        The alpha value at which the animation finishes.
    """
    def __init__(
        self,
        vmobject: VMobject,
        rate_func: Callable[[float], float] = there_and_back,
        remover: bool = True,
        final_alpha_value: float = 0.5,
        **kwargs
    ):
        super().__init__(
            vmobject,
            rate_func=rate_func,
            remover=remover,
            final_alpha_value=final_alpha_value,
            **kwargs
        )
