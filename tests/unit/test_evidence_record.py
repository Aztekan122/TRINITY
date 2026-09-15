from datetime import datetime, timezone

import pytest

from core.evidence.evidence_record import (
    EvidenceRecord,
    EvidenceValidationError,
    validate_evidence_record,
)


def make_evidence() -> EvidenceRecord:
    return EvidenceRecord(
        evidence_id="EV-0001",
        timestamp=datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc),
        evidence_type="correlation",
        subject_id="VESSEL-001",
        source="AIS-A",
        reason="explicit_entity_id_match",
        strength=1.0,
        provenance={
            "event_id": "AIS-A-VESSEL-001-0001",
        },
        context={
            "system_state": "READY",
        },
    )


def test_valid_evidence_record():
    record = make_evidence()

    validate_evidence_record(record)

    assert record.evidence_id == "EV-0001"
    assert record.subject_id == "VESSEL-001"
    assert record.strength == 1.0


def test_evidence_requires_reason():
    record = EvidenceRecord(
        evidence_id="EV-0002",
        timestamp=datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc),
        evidence_type="correlation",
        subject_id="VESSEL-001",
        source="AIS-A",
        reason="",
        strength=1.0,
    )

    with pytest.raises(EvidenceValidationError):
        validate_evidence_record(record)


def test_evidence_strength_must_be_between_zero_and_one():
    record = EvidenceRecord(
        evidence_id="EV-0003",
        timestamp=datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc),
        evidence_type="correlation",
        subject_id="VESSEL-001",
        source="AIS-A",
        reason="test",
        strength=1.1,
    )

    with pytest.raises(EvidenceValidationError):
        validate_evidence_record(record)


def test_evidence_is_immutable():
    record = make_evidence()

    with pytest.raises(AttributeError):
        record.strength = 0.5
