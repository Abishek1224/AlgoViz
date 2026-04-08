from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    width: int = 1100
    height: int = 700
    fps: int = 60
    title: str = "AlgoViz - Phase 2"
    array_size: int = 60
    min_value: int = 10
    max_value: int = 500


class Colors:
    BG = (18, 18, 24)
    PANEL = (28, 33, 48)
    TEXT = (240, 240, 240)
    MUTED = (170, 170, 170)
    BAR = (98, 177, 255)
    COMPARE = (255, 210, 95)
    SWAP = (255, 120, 120)
    SORTED = (112, 223, 130)
    BUTTON = (70, 90, 130)
    BUTTON_HOVER = (85, 108, 155)
    SLIDER = (200, 200, 200)
    SLIDER_KNOB = (255, 255, 255)


class LightColors:
    BG = (242, 245, 251)
    PANEL = (221, 229, 244)
    TEXT = (24, 30, 40)
    MUTED = (90, 100, 120)
    BAR = (69, 136, 214)
    COMPARE = (224, 170, 55)
    SWAP = (210, 95, 95)
    SORTED = (72, 160, 92)
    BUTTON = (130, 150, 195)
    BUTTON_HOVER = (112, 135, 182)
    SLIDER = (70, 80, 100)
    SLIDER_KNOB = (245, 245, 245)
