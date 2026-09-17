from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HistoricalKnowledge:
    """A previously recorded observation or validated scenario.

    Historical knowledge provides context for future assessments.
    It does not establish that the current situation is identical
    to the historical situation.
    """

    knowledge_id: str
    entity_id: str | None
    recorded_at: datetime
    scenario: str
    description: str
    source: str
    confidence: float

    def is_valid_confidence(self) -> bool:
        """Return whether the confidence value is within the valid range."""

        return 0.0 <= self.confidence <= 1.0


