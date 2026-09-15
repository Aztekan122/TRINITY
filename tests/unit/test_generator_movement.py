from datetime import datetime, timezone

from ingestion.synthetic.generator import generate_vessel_track


def test_generated_track_is_deterministic():
    start = datetime(2026, 9, 15, 12, 0, 0, tzinfo=timezone.utc)

    events_a = list(
        generate_vessel_track(
            entity_id="VESSEL-001",
            source="synthetic-A",
            start_time=start,
            latitude=51.45,
            longitude=1.35,
            speed=12.5,
            heading=87.0,
            count=10,
            interval_seconds=60,
        )
    )

    events_b = list(
        generate_vessel_track(
            entity_id="VESSEL-001",
            source="synthetic-A",
            start_time=start,
            latitude=51.45,
            longitude=1.35,
            speed=12.5,
            heading=87.0,
            count=10,
            interval_seconds=60,
        )
    )

    assert events_a == events_b
