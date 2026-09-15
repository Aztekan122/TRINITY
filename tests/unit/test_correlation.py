from datetime import datetime, timedelta, timezone

from core.correlation.correlator import correlate_events
from core.models.maritime_event import MaritimeEvent


def test_correlate_events_by_entity_id():
    start = datetime(2026, 9, 15, 12, 0, 0, tzinfo=timezone.utc)

    events = [
        MaritimeEvent(
            event_id="A-001",
            timestamp=start,
            source="source-A",
            event_type="position",
            entity_id="VESSEL-001",
            latitude=51.45,
            longitude=1.35,
        ),
        MaritimeEvent(
            event_id="B-001",
            timestamp=start + timedelta(minutes=1),
            source="source-B",
            event_type="position",
            entity_id="VESSEL-001",
            latitude=51.46,
            longitude=1.36,
        ),
        MaritimeEvent(
            event_id="A-002",
            timestamp=start + timedelta(minutes=1),
            source="source-A",
            event_type="position",
            entity_id="VESSEL-002",
            latitude=51.50,
            longitude=1.40,
        ),
    ]

    tracks = correlate_events(events)

    assert set(tracks) == {"VESSEL-001", "VESSEL-002"}

    vessel_001 = tracks["VESSEL-001"]

    assert vessel_001.observation_count == 2
    assert vessel_001.events[0].source == "source-A"
    assert vessel_001.events[1].source == "source-B"

    vessel_002 = tracks["VESSEL-002"]

    assert vessel_002.observation_count == 1
