from datetime import datetime, timezone

from core.correlation.assessment import CorrelationAssessment
from core.evidence.evidence_record import (
    EvidenceRecord,
    validate_evidence_record,
)


def assessment_to_evidence(
    assessment: CorrelationAssessment,
    *,
    source: str = "trinity.correlation",
) -> list[EvidenceRecord]:
    """Convert correlation assessment reasons into auditable evidence records."""

    timestamp = datetime.now(timezone.utc)

    evidence: list[EvidenceRecord] = []

    for index, reason in enumerate(assessment.reasons, start=1):
        record = EvidenceRecord(
            evidence_id=(
                f"CORR-{assessment.first_event_id}-"
                f"{assessment.second_event_id}-{index:04d}"
            ),
            timestamp=timestamp,
            evidence_type="correlation",
            subject_id=assessment.first_event_id,
            source=source,
            reason=reason,
            strength=1.0,
            provenance={
                "first_event_id": assessment.first_event_id,
                "second_event_id": assessment.second_event_id,
            },
            context={
                "compatible": assessment.compatible,
            },
        )

        validate_evidence_record(record)
        evidence.append(record)

    return evidence
