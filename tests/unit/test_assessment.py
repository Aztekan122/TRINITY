from datetime import datetime, timedelta, timezone

from core.correlation.assessment import assess_event_pair
from core.models.maritime_event import MaritimeEvent


def make_event(
    event_id: str,
    timestamp: datetime,
    entity_id: str | None,
    latitude: float | None,
    longitude: float | None,
) -> MaritimeEvent:
    return MaritimeEvent(
        event_id=event_id,
        timestamp=timestamp,
        source="test-source",
        event_type="position",
        entity_id=entity_id,
        latitude=latitude,
        longitude=longitude,
    )


def test_explicit_entity_id_match_is_compatible():
    start = datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)

    first = make_event(
        "A-001",
        start,
        "VESSEL-001",
        51.450,
        1.350,
    )

    second = make_event(
        "B-001",
        start + timedelta(minutes=1),
        "VESSEL-001",
        52.000,
        2.000,
    )

    assessment = assess_event_pair(first, second)

    assert assessment.compatible
    assert "explicit_entity_id_match" in assessment.reasons


def test_spatiotemporal_match_is_compatible_without_matching_entity_id():
    start = datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)

    first = make_event(
        "A-001",
        start,
        "VESSEL-A",
        51.450,
        1.350,
    )

    second = make_event(
        "B-001",
        start + timedelta(minutes=1),
        "VESSEL-B",
        51.451,
        1.351,
    )

    assessment = assess_event_pair(first, second)

    assert assessment.compatible
    assert assessment.reasons == ("spatiotemporal_compatibility",)


def test_distant_observations_are_not_compatible():
    start = datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)

    first = make_event(
        "A-001",
        start,
        "VESSEL-A",
        51.450,
        1.350,
    )

    second = make_event(
        "B-001",
        start + timedelta(minutes=1),
        "VESSEL-B",
        55.000,
        5.000,
    )

    assessment = assess_event_pair(first, second)

    assert not assessment.compatible
    assert assessment.reasons == ()


def test_missing_coordinates_prevent_spatiotemporal_match():
    start = datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)

    first = make_event(
        "A-001",
        start,
        "VESSEL-A",
        None,
        None,
    )

    second = make_event(
        "B-001",
        start + timedelta(minutes=1),
        "VESSEL-B",
        51.451,
        1.351,
    )

    assessment = assess_event_pair(first, second)

    assert not assessment.compatible
    assert assessment.reasons == ()
