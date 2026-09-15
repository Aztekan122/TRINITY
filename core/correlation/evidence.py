from dataclasses import dataclass


@dataclass(frozen=True)
class CorrelationEvidence:
    entity_id: str
    source: str
    reason: str
    strength: float
