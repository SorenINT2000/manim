from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable

    from manimlib.event_handler.event_type import EventType
    from manimlib.mobject.mobject import Mobject


class EventListener(object):
    """
    A class that listens for events.

    This class is used to create event listeners. An event listener is a
    callable object that is called when an event of a certain type occurs on
    a certain mobject.

    Parameters
    ----------
    mobject
        The mobject to listen for events on.
    event_type
        The type of event to listen for.
    event_callback
        The function to call when the event occurs.
    """
    def __init__(
        self,
        mobject: Mobject,
        event_type: EventType,
        event_callback: Callable[[Mobject, dict[str]]]
    ):
        self.mobject = mobject
        self.event_type = event_type
        self.callback = event_callback

    def __eq__(self, o: object) -> bool:
        return_val = False
        try:
            return_val = self.callback == o.callback \
                and self.mobject == o.mobject \
                and self.event_type == o.event_type
        except:
            pass
        return return_val
