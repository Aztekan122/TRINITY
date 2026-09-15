from datetime import timedelta

from core.models.maritime_event import MaritimeEvent


def observations_are_spatiotemporally_compatible(
    first: MaritimeEvent,
    second: MaritimeEvent,
    max_time_delta: timedelta = timedelta(minutes=5),
    max_distance_degrees: float = 0.05,
) -> bool:
    """
    Determine whether two observations are compatible in time and position.

    This is a deliberately simple deterministic baseline.
    It is not a physical vessel-motion model.
    """

    if first.latitude is None or first.longitude is None:
        return False

    if second.latitude is None or second.longitude is None:
        return False

    time_delta = abs(first.timestamp - second.timestamp)

    if time_delta > max_time_delta:
        return False

    latitude_delta = abs(first.latitude - second.latitude)
    longitude_delta = abs(first.longitude - second.longitude)

    return (
        latitude_delta <= max_distance_degrees
        and longitude_delta <= max_distance_degrees
    )
