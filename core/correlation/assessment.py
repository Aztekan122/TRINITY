from dataclasses import dataclass

from core.models.maritime_event import MaritimeEvent
from core.correlation.spatial_temporal import (
    observations_are_spatiotemporally_compatible,
)


@dataclass(frozen=True)
class CorrelationAssessment:
    first_event_id: str
    second_event_id: str
    compatible: bool
    reasons: tuple[str, ...]


def assess_event_pair(
    first: MaritimeEvent,
    second: MaritimeEvent,
) -> CorrelationAssessment:
    reasons: list[str] = []

    if (
        first.entity_id
        and second.entity_id
        and first.entity_id == second.entity_id
    ):
        reasons.append("explicit_entity_id_match")

    spatial_temporal_match = observations_are_spatiotemporally_compatible(
        first,
        second,
    )

    if spatial_temporal_match:
        reasons.append("spatiotemporal_compatibility")

    compatible = bool(reasons)

    return CorrelationAssessment(
        first_event_id=first.event_id,
        second_event_id=second.event_id,
        compatible=compatible,
        reasons=tuple(reasons),
    )
