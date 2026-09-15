from datetime import datetime, timezone

from core.correlation.correlator import explain_entity_correlation
from core.models.maritime_event import MaritimeEvent


def test_explicit_entity_id_produces_correlation_evidence():
    event = MaritimeEvent(
        event_id="A-001",
        timestamp=datetime(
            2026,
            9,
            15,
            12,
            0,
            tzinfo=timezone.utc,
        ),
        source="source-A",
        event_type="position",
        entity_id="VESSEL-001",
    )

    evidence = explain_entity_correlation(
        [event],
        "VESSEL-001",
    )

    assert len(evidence) == 1
    assert evidence[0].entity_id == "VESSEL-001"
    assert evidence[0].source == "source-A"
    assert evidence[0].reason == "explicit_entity_id_match"
    assert evidence[0].strength == 1.0
