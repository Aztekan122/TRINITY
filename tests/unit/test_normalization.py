from datetime import datetime, timezone, timedelta

from core.models.maritime_event import MaritimeEvent
from core.models.normalization import normalize_maritime_event


def test_normalizes_maritime_event():
    event = MaritimeEvent(
        event_id=" TEST-001 ",
        timestamp=datetime(
            2026, 9, 15, 12, 0, 0,
            tzinfo=timezone(timedelta(hours=1)),
        ),
        source="  Synthetic-A  ",
        event_type=" POSITION ",
        entity_id=" VESSEL-001 ",
        latitude=51.45,
        longitude=1.35,
        speed=12.5,
        heading=447.0,
        metadata={"original_source": "Synthetic-A"},
    )

    result = normalize_maritime_event(event)

    assert result.event_id == "TEST-001"
    assert result.source == "Synthetic-A"
    assert result.event_type == "position"
    assert result.entity_id == "VESSEL-001"
    assert result.timestamp == datetime(
        2026, 9, 15, 11, 0, 0, tzinfo=timezone.utc
    )
    assert result.heading == 87.0
    assert result.latitude == 51.45
    assert result.longitude == 1.35
    assert result.metadata["original_source"] == "Synthetic-A"
