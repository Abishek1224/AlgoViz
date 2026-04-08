from dataclasses import dataclass
from typing import Callable, Tuple

import pygame

@dataclass
class Button:
    text: str
    rect: pygame.Rect
    on_click: Callable[[], None]

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, mouse_pos: Tuple[int, int], colors: object) -> None:
        hovered = self.rect.collidepoint(mouse_pos)
        color = colors.BUTTON_HOVER if hovered else colors.BUTTON
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        label = font.render(self.text, True, colors.TEXT)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            self.on_click()


@dataclass
class Slider:
    rect: pygame.Rect
    min_val: float
    max_val: float
    value: float
    dragging: bool = False

    def draw(self, surface: pygame.Surface, colors: object) -> None:
        y = self.rect.centery
        pygame.draw.line(surface, colors.SLIDER, (self.rect.left, y), (self.rect.right, y), 4)
        knob_x = int(self.rect.left + ((self.value - self.min_val) / (self.max_val - self.min_val)) * self.rect.width)
        pygame.draw.circle(surface, colors.SLIDER_KNOB, (knob_x, y), 9)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            self.dragging = True
            self._update_value(event.pos[0])
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

    def _update_value(self, mouse_x: int) -> None:
        clamped = max(self.rect.left, min(mouse_x, self.rect.right))
        ratio = (clamped - self.rect.left) / max(1, self.rect.width)
        self.value = self.min_val + ratio * (self.max_val - self.min_val)


@dataclass
class TextInput:
    rect: pygame.Rect
    text: str = ""
    active: bool = False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, colors: object) -> None:
        border_color = colors.BUTTON_HOVER if self.active else colors.MUTED
        pygame.draw.rect(surface, colors.PANEL, self.rect, border_radius=8)
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=8)
        display = self.text if self.text else "Type numbers: 5,1,9,3"
        text_color = colors.TEXT if self.text else colors.MUTED
        label = font.render(display, True, text_color)
        clipped = label
        if label.get_width() > self.rect.width - 10:
            clipped = font.render(display[-28:], True, text_color)
        surface.blit(clipped, (self.rect.x + 6, self.rect.y + 7))

    def handle_event(self, event: pygame.event.Event) -> bool:
        submitted = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                submitted = True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode and len(self.text) < 120:
                self.text += event.unicode
        return submitted
