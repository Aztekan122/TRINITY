from dataclasses import dataclass
from datetime import timedelta

from core.models.track import VesselTrack


@dataclass(frozen=True)
class LoiteringAssessment:
    entity_id: str
    detected: bool
    reasons: tuple[str, ...]
    observation_count: int
    duration: timedelta | None


def assess_loitering(
    track: VesselTrack,
    *,
    minimum_duration: timedelta = timedelta(minutes=20),
    maximum_latitude_span: float = 0.02,
    maximum_longitude_span: float = 0.02,
) -> LoiteringAssessment:
    """Assess whether a vessel track exhibits bounded-area loitering."""

    if not track.events:
        return LoiteringAssessment(
            entity_id=track.entity_id,
            detected=False,
            reasons=("no_observations",),
            observation_count=0,
            duration=None,
        )

    start_time = track.start_time
    end_time = track.end_time

    duration = (
        end_time - start_time
        if start_time is not None and end_time is not None
        else None
    )

    coordinates = [
        (event.latitude, event.longitude)
        for event in track.events
        if event.latitude is not None and event.longitude is not None
    ]

    reasons: list[str] = []

    if duration is None or duration < minimum_duration:
        reasons.append("insufficient_duration")

    if not coordinates:
        reasons.append("no_position_observations")
        detected = False
    else:
        latitudes = [latitude for latitude, _ in coordinates]
        longitudes = [longitude for _, longitude in coordinates]

        latitude_span = max(latitudes) - min(latitudes)
        longitude_span = max(longitudes) - min(longitudes)

        if latitude_span <= maximum_latitude_span:
            reasons.append("bounded_latitude_span")
        else:
            reasons.append("latitude_span_exceeded")

        if longitude_span <= maximum_longitude_span:
            reasons.append("bounded_longitude_span")
        else:
            reasons.append("longitude_span_exceeded")

        detected = (
            duration is not None
            and duration >= minimum_duration
            and latitude_span <= maximum_latitude_span
            and longitude_span <= maximum_longitude_span
        )

    return LoiteringAssessment(
        entity_id=track.entity_id,
        detected=detected,
        reasons=tuple(reasons),
        observation_count=track.observation_count,
        duration=duration,
    )
