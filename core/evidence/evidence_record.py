from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


class EvidenceValidationError(ValueError):
    """Raised when an evidence record violates the TRINITY evidence contract."""


@dataclass(frozen=True)
class EvidenceRecord:
    """
    Immutable record describing evidence used by TRINITY.

    Evidence records are deliberately explicit and auditable. They identify
    what was observed, where it came from, why it matters, and the context
    under which TRINITY recorded it.
    """

    evidence_id: str
    timestamp: datetime
    evidence_type: str
    subject_id: str | None
    source: str
    reason: str
    strength: float
    provenance: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)


def validate_evidence_record(record: EvidenceRecord) -> None:
    """Validate the TRINITY evidence contract."""

    if not record.evidence_id:
        raise EvidenceValidationError("evidence_id is required")

    if not record.evidence_type:
        raise EvidenceValidationError("evidence_type is required")

    if not record.source:
        raise EvidenceValidationError("source is required")

    if not record.reason:
        raise EvidenceValidationError("reason is required")

    if not 0.0 <= record.strength <= 1.0:
        raise EvidenceValidationError(
            "strength must be between 0 and 1"
        )
