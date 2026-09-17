from datetime import datetime, timedelta

from core.history.knowledge import HistoricalKnowledge


def find_historical_knowledge(
    knowledge: list[HistoricalKnowledge],
    entity_id: str,
    *,
    reference_time: datetime | None = None,
    time_window: timedelta | None = None,
) -> list[HistoricalKnowledge]:
    """Return relevant historical knowledge associated with an entity.

    Historical records provide context only. This function does not
    determine whether a historical scenario describes the current
    situation.

    If reference_time and time_window are supplied, only records within
    that time window before the reference time are returned.

    No default retention period is imposed.
    """

    records = [
        record
        for record in knowledge
        if record.entity_id == entity_id
    ]

    if reference_time is None or time_window is None:
        return records

    if time_window < timedelta(0):
        raise ValueError("time_window must not be negative")

    earliest_time = reference_time - time_window

    return [
        record
        for record in records
        if earliest_time <= record.recorded_at <= reference_time
    ]
