from datetime import datetime, timedelta, timezone

import pytest

from core.history.knowledge import HistoricalKnowledge
from core.history.lookup import find_historical_knowledge


def make_knowledge(
    knowledge_id: str,
    entity_id: str,
    scenario: str,
    recorded_at: datetime | None = None,
) -> HistoricalKnowledge:
    return HistoricalKnowledge(
        knowledge_id=knowledge_id,
        entity_id=entity_id,
        recorded_at=recorded_at or datetime(
            2026,
            9,
            15,
            12,
            0,
            tzinfo=timezone.utc,
        ),
        scenario=scenario,
        description=f"Historical {scenario} observation.",
        source="validated_observation",
        confidence=0.90,
    )


def test_lookup_returns_historical_knowledge_for_entity():
    knowledge = [
        make_knowledge(
            "HK-001",
            "VESSEL-001",
            "loitering",
        ),
        make_knowledge(
            "HK-002",
            "VESSEL-002",
            "rendezvous",
        ),
    ]

    results = find_historical_knowledge(
        knowledge,
        "VESSEL-001",
    )

    assert len(results) == 1
    assert results[0].knowledge_id == "HK-001"
    assert results[0].scenario == "loitering"


def test_lookup_does_not_return_other_entities():
    knowledge = [
        make_knowledge(
            "HK-001",
            "VESSEL-001",
            "loitering",
        ),
        make_knowledge(
            "HK-002",
            "VESSEL-002",
            "rendezvous",
        ),
    ]

    results = find_historical_knowledge(
        knowledge,
        "VESSEL-003",
    )

    assert results == []


def test_lookup_can_return_multiple_historical_records():
    knowledge = [
        make_knowledge(
            "HK-001",
            "VESSEL-001",
            "loitering",
        ),
        make_knowledge(
            "HK-002",
            "VESSEL-001",
            "route_deviation",
        ),
        make_knowledge(
            "HK-003",
            "VESSEL-002",
            "rendezvous",
        ),
    ]

    results = find_historical_knowledge(
        knowledge,
        "VESSEL-001",
    )

    assert len(results) == 2
    assert {record.knowledge_id for record in results} == {
        "HK-001",
        "HK-002",
    }


def test_lookup_returns_context_without_changing_historical_knowledge():
    knowledge = [
        make_knowledge(
            "HK-001",
            "VESSEL-001",
            "loitering",
        ),
    ]

    results = find_historical_knowledge(
        knowledge,
        "VESSEL-001",
    )

    assert results[0].scenario == "loitering"
    assert results[0].confidence == 0.90
    assert not hasattr(results[0], "current_truth")


def test_lookup_includes_record_exactly_at_reference_time():
    reference_time = datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)

    knowledge = [
        make_knowledge(
            "HK-001",
            "VESSEL-001",
            "loitering",
            recorded_at=reference_time,
        ),
    ]

    results = find_historical_knowledge(
        knowledge,
        "VESSEL-001",
        reference_time=reference_time,
        time_window=timedelta(hours=1),
    )

    assert [record.knowledge_id for record in results] == ["HK-001"]


def test_lookup_includes_record_exactly_at_earliest_boundary():
    reference_time = datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)
    earliest_time = reference_time - timedelta(hours=1)

    knowledge = [
        make_knowledge(
            "HK-001",
            "VESSEL-001",
            "loitering",
            recorded_at=earliest_time,
        ),
    ]

    results = find_historical_knowledge(
        knowledge,
        "VESSEL-001",
        reference_time=reference_time,
        time_window=timedelta(hours=1),
    )

    assert [record.knowledge_id for record in results] == ["HK-001"]


def test_lookup_excludes_record_just_before_earliest_boundary():
    reference_time = datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)
    recorded_at = reference_time - timedelta(hours=1, seconds=1)

    knowledge = [
        make_knowledge(
            "HK-001",
            "VESSEL-001",
            "loitering",
            recorded_at=recorded_at,
        ),
    ]

    results = find_historical_knowledge(
        knowledge,
        "VESSEL-001",
        reference_time=reference_time,
        time_window=timedelta(hours=1),
    )

    assert results == []


def test_lookup_excludes_record_after_reference_time():
    reference_time = datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)
    recorded_at = reference_time + timedelta(seconds=1)

    knowledge = [
        make_knowledge(
            "HK-001",
            "VESSEL-001",
            "loitering",
            recorded_at=recorded_at,
        ),
    ]

    results = find_historical_knowledge(
        knowledge,
        "VESSEL-001",
        reference_time=reference_time,
        time_window=timedelta(hours=1),
    )

    assert results == []


def test_lookup_rejects_negative_time_window():
    reference_time = datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)

    with pytest.raises(ValueError, match="time_window must not be negative"):
        find_historical_knowledge(
            [],
            "VESSEL-001",
            reference_time=reference_time,
            time_window=timedelta(seconds=-1),
        )


def test_lookup_without_time_filter_returns_all_entity_records():
    knowledge = [
        make_knowledge(
            "HK-001",
            "VESSEL-001",
            "loitering",
        ),
        make_knowledge(
            "HK-002",
            "VESSEL-001",
            "route_deviation",
        ),
    ]

    results = find_historical_knowledge(
        knowledge,
        "VESSEL-001",
    )

    assert {record.knowledge_id for record in results} == {
        "HK-001",
        "HK-002",
    }
