"""Utility functions for wall clocks."""


def time_str(hour, minute):
    """Convert a 24-hour time to a 12-hour time format.

    Args:
        hour (int): The hour in 24-hour format (0--23).
        minute (int): The minute (0--59).

    Returns:
        str: The time in 12-hour format including AM/PM.
             Ex: "03:15 PM", or "12:00 AM" for midnight.
    """
    if hour < 12:
        ampm = "AM"
        if hour == 0:
            hour = 12  # midnight
    else:
        ampm = "PM"
        hour -= 12
    return f"{hour:02d}:{minute:02d} {ampm}"


def add_time(hour, minute, delta):
    """Determine what time it is after delta minutes.

    Args:
        hour (int): The starting hour in 24-hour format (0--23).
        minute (int): The starting minute (0--59).
        delta (int): How many minutes to add (can be negative).

    Returns:
        str: The resulting time in 12-hour format.
    """
    time = hour*60 + minute + delta
    hour = time // 60 % 24
    minute = time % 60
    return time_str(hour, minute)
