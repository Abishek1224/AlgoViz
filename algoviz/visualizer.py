from typing import List, Set, Tuple

import pygame

class ArrayRenderer:
    def __init__(self, area: pygame.Rect, max_value: int) -> None:
        self.area = area
        self.max_value = max_value

    def draw(
        self,
        surface: pygame.Surface,
        values: List[int],
        active_indices: Tuple[int, int],
        event_kind: str,
        sorted_indices: Set[int],
        colors: object,
    ) -> None:
        count = len(values)
        if count == 0:
            return

        bar_width = max(3, self.area.width // count)
        gap = 1

        for idx, value in enumerate(values):
            x = self.area.left + idx * bar_width
            normalized = value / max(1, self.max_value)
            h = int(normalized * self.area.height)
            y = self.area.bottom - h

            color = colors.BAR
            if idx in sorted_indices:
                color = colors.SORTED
            if idx in active_indices:
                color = colors.COMPARE if event_kind == "compare" else colors.SWAP

            pygame.draw.rect(surface, color, (x, y, max(1, bar_width - gap), h), border_radius=2)
