from dataclasses import dataclass, field
from datetime import datetime

from core.models.maritime_event import MaritimeEvent


@dataclass
class VesselTrack:
    entity_id: str
    events: list[MaritimeEvent] = field(default_factory=list)

    @property
    def start_time(self) -> datetime | None:
        return self.events[0].timestamp if self.events else None

    @property
    def end_time(self) -> datetime | None:
        return self.events[-1].timestamp if self.events else None

    @property
    def observation_count(self) -> int:
        return len(self.events)
