from datetime import datetime, timedelta, timezone

from core.models.maritime_event import MaritimeEvent
from core.correlation.spatial_temporal import (
    observations_are_spatiotemporally_compatible,
)


def make_event(
    event_id: str,
    timestamp: datetime,
    latitude: float,
    longitude: float,
) -> MaritimeEvent:
    return MaritimeEvent(
        event_id=event_id,
        timestamp=timestamp,
        source="test-source",
        event_type="position",
        latitude=latitude,
        longitude=longitude,
    )


def test_observations_are_spatiotemporally_compatible():
    start = datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)

    first = make_event(
        "A-001",
        start,
        51.450,
        1.350,
    )

    second = make_event(
        "B-001",
        start + timedelta(minutes=1),
        51.451,
        1.351,
    )

    assert observations_are_spatiotemporally_compatible(
        first,
        second,
    )


def test_observations_are_not_compatible_when_too_far_apart():
    start = datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)

    first = make_event(
        "A-001",
        start,
        51.450,
        1.350,
    )

    second = make_event(
        "B-001",
        start + timedelta(minutes=1),
        55.000,
        5.000,
    )

    assert not observations_are_spatiotemporally_compatible(
        first,
        second,
    )
