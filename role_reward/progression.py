"""Pure helpers for turning a configured progression into a reward threshold."""

from __future__ import annotations

import math


def required_distinct_balls(total_balls: int, progression: float) -> int:
    """Return how many distinct enabled balls a player needs to be eligible.

    The threshold is rounded up so that even a small progression always requires
    at least one ball and no configuration can demand more balls than exist.
    """
    if total_balls < 0:
        raise ValueError("Total number of balls cannot be negative.")
    if not 0 < progression <= 1:
        raise ValueError("Progression must be greater than 0% and at most 100%.")
    return math.ceil(total_balls * progression)
