from dataclasses import dataclass
from typing import Tuple


@dataclass
class StepEvent:
    kind: str
    indices: Tuple[int, int]


@dataclass
class Metrics:
    comparisons: int = 0
    swaps: int = 0
    steps: int = 0

    def reset(self) -> None:
        self.comparisons = 0
        self.swaps = 0
        self.steps = 0
