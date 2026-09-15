from datetime import datetime, timezone

from ingestion.synthetic.generator import generate_vessel_track


def test_generate_vessel_track():
    start = datetime(2026, 9, 15, 12, 0, 0, tzinfo=timezone.utc)

    events = list(
        generate_vessel_track(
            entity_id="VESSEL-001",
            source="synthetic-A",
            start_time=start,
            latitude=51.45,
            longitude=1.35,
            speed=12.5,
            heading=87.0,
            count=5,
            interval_seconds=60,
        )
    )

    assert len(events) == 5

    assert events[0].event_id == "synthetic-A-VESSEL-001-0000"
    assert events[4].event_id == "synthetic-A-VESSEL-001-0004"

    assert events[0].timestamp == start
    assert events[1].timestamp == datetime(
        2026, 9, 15, 12, 1, 0, tzinfo=timezone.utc
    )
    assert events[4].timestamp == datetime(
        2026, 9, 15, 12, 4, 0, tzinfo=timezone.utc
    )

    assert all(event.entity_id == "VESSEL-001" for event in events)
    assert all(event.source == "synthetic-A" for event in events)
    assert all(event.event_type == "position" for event in events)
    assert all(event.metadata["synthetic"] is True for event in events)
