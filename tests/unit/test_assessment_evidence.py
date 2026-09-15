from core.correlation.assessment import CorrelationAssessment
from core.evidence.assessment_evidence import assessment_to_evidence
from core.evidence.evidence_record import EvidenceRecord


def make_assessment() -> CorrelationAssessment:
    return CorrelationAssessment(
        first_event_id="EV-001",
        second_event_id="EV-002",
        compatible=True,
        reasons=(
            "explicit_entity_id_match",
            "spatiotemporal_compatibility",
        ),
    )


def test_assessment_to_evidence_creates_one_record_per_reason():
    assessment = make_assessment()

    evidence = assessment_to_evidence(
        assessment,
        source="TRINITY-CORRELATOR",
    )

    assert len(evidence) == 2
    assert all(isinstance(record, EvidenceRecord) for record in evidence)


def test_assessment_evidence_preserves_event_relationship():
    assessment = make_assessment()

    evidence = assessment_to_evidence(
        assessment,
        source="TRINITY-CORRELATOR",
    )

    assert evidence[0].provenance["first_event_id"] == "EV-001"
    assert evidence[0].provenance["second_event_id"] == "EV-002"


def test_assessment_evidence_preserves_reason_and_compatibility():
    assessment = make_assessment()

    evidence = assessment_to_evidence(
        assessment,
        source="TRINITY-CORRELATOR",
    )

    assert evidence[0].reason == "explicit_entity_id_match"
    assert evidence[1].reason == "spatiotemporal_compatibility"
    assert evidence[0].context["compatible"] is True
    assert evidence[1].context["compatible"] is True


def test_assessment_evidence_has_valid_strength_and_unique_ids():
    assessment = make_assessment()

    evidence = assessment_to_evidence(
        assessment,
        source="TRINITY-CORRELATOR",
    )

    assert all(record.strength == 1.0 for record in evidence)
    assert len({record.evidence_id for record in evidence}) == len(evidence)
