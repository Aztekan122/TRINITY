from datetime import datetime, timedelta, timezone
from typing import Iterator

from core.models.maritime_event import MaritimeEvent


def generate_vessel_track(
    entity_id: str,
    source: str,
    start_time: datetime,
    latitude: float,
    longitude: float,
    speed: float,
    heading: float,
    count: int = 10,
    interval_seconds: int = 60,
) -> Iterator[MaritimeEvent]:
    """
    Generate a deterministic synthetic position stream for one vessel.
    """

    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)
    else:
        start_time = start_time.astimezone(timezone.utc)

    for index in range(count):
        timestamp = start_time + timedelta(
            seconds=index * interval_seconds
        )

        yield MaritimeEvent(
            event_id=f"{source}-{entity_id}-{index:04d}",
            timestamp=timestamp,
            source=source,
            event_type="position",
            entity_id=entity_id,
            latitude=latitude,
            longitude=longitude,
            speed=speed,
            heading=heading,
            metadata={
                "synthetic": True,
                "sequence": index,
            },
        )
