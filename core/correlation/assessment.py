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


@dataclass(frozen=True)
class EntityRelationship:
    first_entity_id: str
    second_entity_id: str
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


def assess_entity_relationship(
    first: MaritimeEvent,
    second: MaritimeEvent,
) -> EntityRelationship | None:
    """Assess a relationship between two distinct entities.

    This does not merge identities. It records whether observations
    associated with different entities are compatible in time and space.
    """

    if not first.entity_id or not second.entity_id:
        return None

    if first.entity_id == second.entity_id:
        return None

    assessment = assess_event_pair(first, second)

    if not assessment.compatible:
        return None

    return EntityRelationship(
        first_entity_id=first.entity_id,
        second_entity_id=second.entity_id,
        compatible=True,
        reasons=assessment.reasons,
    )




