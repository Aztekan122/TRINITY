from dataclasses import dataclass


@dataclass(frozen=True)
class MovementStep:
    latitude_delta: float
    longitude_delta: float
