from datetime import datetime, timezone

from core.models.track import VesselTrack
from ingestion.synthetic.generator import generate_vessel_track


def test_vessel_track():
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

    track = VesselTrack(
        entity_id="VESSEL-001",
        events=events,
    )

    assert track.entity_id == "VESSEL-001"
    assert track.observation_count == 5
    assert track.start_time == events[0].timestamp
    assert track.end_time == events[-1].timestamp
