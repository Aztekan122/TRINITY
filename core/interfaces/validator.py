from dataclasses import asdict
from typing import Any

from core.models.maritime_event import MaritimeEvent


class MaritimeEventValidationError(ValueError):
    """Raised when a maritime event violates the TRINITY event contract."""


def validate_maritime_event(event: MaritimeEvent) -> None:
    if not event.event_id:
        raise MaritimeEventValidationError("event_id is required")

    if not event.source:
        raise MaritimeEventValidationError("source is required")

    if not event.event_type:
        raise MaritimeEventValidationError("event_type is required")

    if event.latitude is not None and not -90.0 <= event.latitude <= 90.0:
        raise MaritimeEventValidationError("latitude must be between -90 and 90")

    if event.longitude is not None and not -180.0 <= event.longitude <= 180.0:
        raise MaritimeEventValidationError("longitude must be between -180 and 180")

    if event.speed is not None and event.speed < 0:
        raise MaritimeEventValidationError("speed cannot be negative")

    if event.heading is not None and not 0.0 <= event.heading < 360.0:
        raise MaritimeEventValidationError("heading must be >= 0 and < 360")


def event_to_dict(event: MaritimeEvent) -> dict[str, Any]:
    validate_maritime_event(event)
    return asdict(event)
