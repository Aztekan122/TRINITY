from datetime import datetime, timezone

from core.history.knowledge import HistoricalKnowledge


def test_historical_knowledge_records_previous_scenario():
    knowledge = HistoricalKnowledge(
        knowledge_id="HK-001",
        entity_id="VESSEL-001",
        recorded_at=datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc),
        scenario="loitering",
        description="Previous bounded-area loitering observation.",
        source="ground_truth",
        confidence=0.95,
    )

    assert knowledge.knowledge_id == "HK-001"
    assert knowledge.entity_id == "VESSEL-001"
    assert knowledge.scenario == "loitering"
    assert knowledge.source == "ground_truth"
    assert knowledge.confidence == 0.95


def test_historical_knowledge_accepts_valid_confidence():
    knowledge = HistoricalKnowledge(
        knowledge_id="HK-002",
        entity_id="VESSEL-002",
        recorded_at=datetime(2026, 9, 15, 13, 0, tzinfo=timezone.utc),
        scenario="rendezvous",
        description="Previous proximity event.",
        source="validated_observation",
        confidence=0.75,
    )

    assert knowledge.is_valid_confidence()


def test_historical_knowledge_rejects_invalid_confidence():
    knowledge = HistoricalKnowledge(
        knowledge_id="HK-003",
        entity_id="VESSEL-003",
        recorded_at=datetime(2026, 9, 15, 14, 0, tzinfo=timezone.utc),
        scenario="route_deviation",
        description="Previous route deviation observation.",
        source="validated_observation",
        confidence=1.5,
    )

    assert not knowledge.is_valid_confidence()


def test_historical_knowledge_does_not_assert_current_truth():
    knowledge = HistoricalKnowledge(
        knowledge_id="HK-004",
        entity_id="VESSEL-004",
        recorded_at=datetime(2026, 9, 15, 15, 0, tzinfo=timezone.utc),
        scenario="loitering",
        description="Previous bounded-area loitering observation.",
        source="validated_observation",
        confidence=0.90,
    )

    assert knowledge.scenario == "loitering"
    assert not hasattr(knowledge, "current_truth")



