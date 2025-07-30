from enum import Enum


class EventType(Enum):
    """
    An enumeration of event types.

    This enumeration defines the different types of events that can be
    dispatched by the event dispatcher.
    """
    MouseMotionEvent = 'mouse_motion_event'
    MousePressEvent = 'mouse_press_event'
    MouseReleaseEvent = 'mouse_release_event'
    MouseDragEvent = 'mouse_drag_event'
    MouseScrollEvent = 'mouse_scroll_event'
    KeyPressEvent = 'key_press_event'
    KeyReleaseEvent = 'key_release_event'
