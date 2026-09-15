from core.correlation.evidence import CorrelationEvidence
from core.models.maritime_event import MaritimeEvent
from core.models.track import VesselTrack


def correlate_events(
    events: list[MaritimeEvent],
) -> dict[str, VesselTrack]:
    """
    Baseline correlation using explicit entity identity.
    """
    tracks: dict[str, VesselTrack] = {}

    for event in events:
        if not event.entity_id:
            continue

        if event.entity_id not in tracks:
            tracks[event.entity_id] = VesselTrack(
                entity_id=event.entity_id,
            )

        tracks[event.entity_id].events.append(event)

    for track in tracks.values():
        track.events.sort(key=lambda event: event.timestamp)

    return tracks


def explain_entity_correlation(
    events: list[MaritimeEvent],
    entity_id: str,
) -> list[CorrelationEvidence]:
    """
    Return explicit evidence supporting observations associated
    with an entity.

    This is deliberately deterministic and transparent.
    """
    evidence: list[CorrelationEvidence] = []

    for event in events:
        if event.entity_id != entity_id:
            continue

        evidence.append(
            CorrelationEvidence(
                entity_id=entity_id,
                source=event.source,
                reason="explicit_entity_id_match",
                strength=1.0,
            )
        )

    return evidence
