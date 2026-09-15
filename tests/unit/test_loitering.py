from datetime import datetime, timedelta, timezone

from core.detection.loitering import assess_loitering
from core.models.maritime_event import MaritimeEvent
from core.models.track import VesselTrack


def make_event(
    event_id: str,
    minutes: int,
    latitude: float | None = 50.0,
    longitude: float | None = 1.0,
) -> MaritimeEvent:
    return MaritimeEvent(
        event_id=event_id,
        timestamp=datetime(
            2026,
            1,
            1,
            12,
            0,
            tzinfo=timezone.utc,
        ) + timedelta(minutes=minutes),
        source="test",
        event_type="position",
        entity_id="VESSEL-001",
        latitude=latitude,
        longitude=longitude,
    )


def test_empty_track_is_not_loitering():
    track = VesselTrack(entity_id="VESSEL-001")

    result = assess_loitering(track)

    assert result.detected is False
    assert result.reasons == ("no_observations",)
    assert result.observation_count == 0
    assert result.duration is None


def test_insufficient_duration_is_not_loitering():
    track = VesselTrack(
        entity_id="VESSEL-001",
        events=[
            make_event("EV-001", 0),
            make_event("EV-002", 10),
        ],
    )

    result = assess_loitering(track)

    assert result.detected is False
    assert "insufficient_duration" in result.reasons


def test_missing_positions_are_not_loitering():
    track = VesselTrack(
        entity_id="VESSEL-001",
        events=[
            make_event("EV-001", 0, None, None),
            make_event("EV-002", 30, None, None),
        ],
    )

    result = assess_loitering(track)

    assert result.detected is False
    assert "no_position_observations" in result.reasons


def test_bounded_twenty_minute_track_is_loitering():
    track = VesselTrack(
        entity_id="VESSEL-001",
        events=[
            make_event("EV-001", 0, 50.000, 1.000),
            make_event("EV-002", 10, 50.005, 1.005),
            make_event("EV-003", 20, 50.010, 1.010),
        ],
    )

    result = assess_loitering(track)

    assert result.detected is True
    assert "bounded_latitude_span" in result.reasons
    assert "bounded_longitude_span" in result.reasons
    assert result.observation_count == 3
    assert result.duration == timedelta(minutes=20)


def test_track_exceeding_latitude_span_is_not_loitering():
    track = VesselTrack(
        entity_id="VESSEL-001",
        events=[
            make_event("EV-001", 0, 50.000, 1.000),
            make_event("EV-002", 10, 50.010, 1.005),
            make_event("EV-003", 20, 50.030, 1.010),
        ],
    )

    result = assess_loitering(track)

    assert result.detected is False
    assert "latitude_span_exceeded" in result.reasons


def test_track_exceeding_longitude_span_is_not_loitering():
    track = VesselTrack(
        entity_id="VESSEL-001",
        events=[
            make_event("EV-001", 0, 50.000, 1.000),
            make_event("EV-002", 10, 50.005, 1.010),
            make_event("EV-003", 20, 50.010, 1.030),
        ],
    )

    result = assess_loitering(track)

    assert result.detected is False
    assert "longitude_span_exceeded" in result.reasons
