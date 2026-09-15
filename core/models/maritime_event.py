from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class MaritimeEvent:
    event_id: str
    timestamp: datetime
    source: str
    event_type: str
    entity_id: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    speed: float | None = None
    heading: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
