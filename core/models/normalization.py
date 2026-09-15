from datetime import timezone

from core.models.maritime_event import MaritimeEvent


def normalize_maritime_event(event: MaritimeEvent) -> MaritimeEvent:
    timestamp = event.timestamp

    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    else:
        timestamp = timestamp.astimezone(timezone.utc)

    source = event.source.strip()
    entity_id = event.entity_id.strip() if event.entity_id else None
    event_type = event.event_type.strip().lower()

    heading = event.heading
    if heading is not None:
        heading = heading % 360.0

    return MaritimeEvent(
        event_id=event.event_id.strip(),
        timestamp=timestamp,
        source=source,
        event_type=event_type,
        entity_id=entity_id,
        latitude=event.latitude,
        longitude=event.longitude,
        speed=event.speed,
        heading=heading,
        metadata=dict(event.metadata),
    )
