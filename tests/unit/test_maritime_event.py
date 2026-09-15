from datetime import datetime, timezone

import pytest

from core.models.maritime_event import MaritimeEvent
from core.interfaces.validator import (
    MaritimeEventValidationError,
    validate_maritime_event,
)


def make_event(**overrides):
    values = {
        "event_id": "TEST-001",
        "timestamp": datetime.now(timezone.utc),
        "source": "synthetic-A",
        "event_type": "position",
        "entity_id": "VESSEL-001",
        "latitude": 51.45,
        "longitude": 1.35,
        "speed": 12.5,
        "heading": 87.0,
    }
    values.update(overrides)
    return MaritimeEvent(**values)


def test_valid_maritime_event():
    event = make_event()

    validate_maritime_event(event)


def test_invalid_latitude():
    event = make_event(latitude=91.0)

    with pytest.raises(MaritimeEventValidationError):
        validate_maritime_event(event)


def test_invalid_longitude():
    event = make_event(longitude=181.0)

    with pytest.raises(MaritimeEventValidationError):
        validate_maritime_event(event)


def test_negative_speed():
    event = make_event(speed=-1.0)

    with pytest.raises(MaritimeEventValidationError):
        validate_maritime_event(event)


def test_invalid_heading():
    event = make_event(heading=360.0)

    with pytest.raises(MaritimeEventValidationError):
        validate_maritime_event(event)
