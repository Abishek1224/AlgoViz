import random
from typing import Callable, Generator, Optional, Set

import pygame

from algoviz.algorithms import ALGORITHMS
from algoviz.config import AppConfig, Colors, LightColors
from algoviz.models import Metrics, StepEvent
from algoviz.ui import Button, Slider, TextInput
from algoviz.visualizer import ArrayRenderer


class AlgoVizApp:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(AppConfig.title)
        self.screen = pygame.display.set_mode((AppConfig.width, AppConfig.height))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Segoe UI", 20)
        self.small_font = pygame.font.SysFont("Segoe UI", 16)
        self.colors = Colors
        self.sound_enabled = False

        self.array_size = AppConfig.array_size
        self.values = self._new_data()
        self.metrics = Metrics()
        self.sorted_indices: Set[int] = set()
        self.current_event = StepEvent("idle", (-1, -1))
        self.algorithm_names = list(ALGORITHMS.keys())
        self.algorithm_index = 0
        self.step_generator: Optional[Generator[StepEvent, None, None]] = None
        self.is_playing = False
        self.accumulated_ms = 0.0

        self.draw_area = pygame.Rect(50, 120, AppConfig.width - 100, AppConfig.height - 220)
        self.renderer = ArrayRenderer(self.draw_area, AppConfig.max_value)
        self.speed_slider = Slider(pygame.Rect(760, 45, 150, 20), 1.0, 60.0, 15.0)
        self.size_slider = Slider(pygame.Rect(920, 45, 130, 20), 20, 120, float(self.array_size))
        self.custom_input = TextInput(pygame.Rect(50, AppConfig.height - 74, 360, 32))
        self.buttons = self._build_buttons()

        self._reset_algorithm_state()

    def _build_buttons(self) -> list[Button]:
        return [
            Button("Play", pygame.Rect(40, 35, 90, 36), self.play),
            Button("Pause", pygame.Rect(140, 35, 90, 36), self.pause),
            Button("Step", pygame.Rect(240, 35, 90, 36), self.step_once),
            Button("Reset", pygame.Rect(340, 35, 90, 36), self.reset_data),
            Button("Shuffle", pygame.Rect(440, 35, 100, 36), self.shuffle_data),
            Button("Prev Algo", pygame.Rect(560, 35, 110, 36), self.prev_algo),
            Button("Next Algo", pygame.Rect(680, 35, 110, 36), self.next_algo),
            Button("Apply Input", pygame.Rect(420, AppConfig.height - 74, 120, 32), self.apply_custom_input),
            Button("Theme", pygame.Rect(550, AppConfig.height - 74, 90, 32), self.toggle_theme),
            Button("Sound", pygame.Rect(650, AppConfig.height - 74, 90, 32), self.toggle_sound),
        ]

    def _new_data(self) -> list[int]:
        return [random.randint(AppConfig.min_value, AppConfig.max_value) for _ in range(self.array_size)]

    def _reset_algorithm_state(self) -> None:
        algo_fn: Callable[[list[int]], Generator[StepEvent, None, None]] = ALGORITHMS[self.algorithm_names[self.algorithm_index]]
        self.step_generator = algo_fn(self.values)
        self.sorted_indices.clear()
        self.metrics.reset()
        self.current_event = StepEvent("idle", (-1, -1))
        self.is_playing = False
        self.accumulated_ms = 0.0

    def play(self) -> None:
        self.is_playing = True

    def pause(self) -> None:
        self.is_playing = False

    def step_once(self) -> None:
        self.is_playing = False
        self._advance_one_step()

    def reset_data(self) -> None:
        self.values = self._new_data()
        self._reset_algorithm_state()

    def shuffle_data(self) -> None:
        random.shuffle(self.values)
        self._reset_algorithm_state()

    def apply_custom_input(self) -> None:
        raw = self.custom_input.text.strip()
        if not raw:
            return
        try:
            values = [int(part.strip()) for part in raw.split(",") if part.strip()]
            if len(values) < 5:
                return
            clamped = [max(AppConfig.min_value, min(v, AppConfig.max_value)) for v in values]
            self.values = clamped[:120]
            self.array_size = len(self.values)
            self.size_slider.value = float(self.array_size)
            self._reset_algorithm_state()
        except ValueError:
            return

    def toggle_theme(self) -> None:
        self.colors = LightColors if self.colors is Colors else Colors

    def toggle_sound(self) -> None:
        self.sound_enabled = not self.sound_enabled

    def prev_algo(self) -> None:
        self.algorithm_index = (self.algorithm_index - 1) % len(self.algorithm_names)
        self._reset_algorithm_state()

    def next_algo(self) -> None:
        self.algorithm_index = (self.algorithm_index + 1) % len(self.algorithm_names)
        self._reset_algorithm_state()

    def _advance_one_step(self) -> None:
        if self.step_generator is None:
            return
        try:
            event = next(self.step_generator)
            self.current_event = event
            self.metrics.steps += 1

            if event.kind == "compare":
                self.metrics.comparisons += 1
            elif event.kind == "swap":
                self.metrics.swaps += 1
            elif event.kind == "mark_sorted":
                self.sorted_indices.add(event.indices[0])
            elif event.kind == "done":
                self.sorted_indices = set(range(len(self.values)))
                self.is_playing = False
        except StopIteration:
            self.is_playing = False

    def _handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            for button in self.buttons:
                button.handle_event(event)
            self.speed_slider.handle_event(event)
            self.size_slider.handle_event(event)
            if self.custom_input.handle_event(event):
                self.apply_custom_input()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.is_playing = not self.is_playing
                elif event.key == pygame.K_RIGHT:
                    self.step_once()
                elif event.key == pygame.K_r:
                    self.reset_data()
        return True

    def _update(self, dt_ms: float) -> None:
        new_size = int(round(self.size_slider.value))
        if not self.size_slider.dragging and new_size != self.array_size:
            self.array_size = new_size
            self.values = self._new_data()
            self._reset_algorithm_state()

        if not self.is_playing:
            return
        self.accumulated_ms += dt_ms
        step_interval_ms = 1000.0 / self.speed_slider.value
        while self.accumulated_ms >= step_interval_ms:
            self._advance_one_step()
            self.accumulated_ms -= step_interval_ms

    def _get_complexity_text(self) -> str:
        algo = self.algorithm_names[self.algorithm_index]
        table = {
            "Bubble Sort": "Best O(n), Avg O(n^2), Worst O(n^2), Stable: Yes",
            "Selection Sort": "Best O(n^2), Avg O(n^2), Worst O(n^2), Stable: No",
            "Insertion Sort": "Best O(n), Avg O(n^2), Worst O(n^2), Stable: Yes",
        }
        return table.get(algo, "Complexity information not available")

    def _draw_header(self) -> None:
        pygame.draw.rect(self.screen, self.colors.PANEL, (20, 20, AppConfig.width - 40, 80), border_radius=12)
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, self.small_font, mouse_pos, self.colors)

        speed_text = self.small_font.render(f"Speed: {self.speed_slider.value:.1f} steps/s", True, self.colors.TEXT)
        size_text = self.small_font.render(f"Size: {self.array_size}", True, self.colors.TEXT)
        self.screen.blit(speed_text, (760, 20))
        self.screen.blit(size_text, (920, 20))
        self.speed_slider.draw(self.screen, self.colors)
        self.size_slider.draw(self.screen, self.colors)

    def _draw_status(self) -> None:
        algo_name = self.algorithm_names[self.algorithm_index]
        status_text = f"Algorithm: {algo_name} | Comparisons: {self.metrics.comparisons} | Swaps: {self.metrics.swaps} | Steps: {self.metrics.steps}"
        text_surface = self.font.render(status_text, True, self.colors.TEXT)
        self.screen.blit(text_surface, (50, 92))

        complexity = self._get_complexity_text()
        complexity_surface = self.small_font.render(f"Complexity: {complexity}", True, self.colors.MUTED)
        self.screen.blit(complexity_surface, (50, 116))

        self.custom_input.draw(self.screen, self.small_font, self.colors)
        sound_label = "Sound: ON" if self.sound_enabled else "Sound: OFF"
        sound_surface = self.small_font.render(sound_label, True, self.colors.MUTED)
        self.screen.blit(sound_surface, (750, AppConfig.height - 68))

        helper = "Controls: Space=Play/Pause, Right Arrow=Step, R=Reset"
        helper_surface = self.small_font.render(helper, True, self.colors.MUTED)
        self.screen.blit(helper_surface, (50, AppConfig.height - 34))

    def _draw(self) -> None:
        self.screen.fill(self.colors.BG)
        self._draw_header()
        self._draw_status()
        self.renderer.draw(
            self.screen,
            self.values,
            self.current_event.indices,
            self.current_event.kind,
            self.sorted_indices,
            self.colors,
        )
        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            dt_ms = self.clock.tick(AppConfig.fps)
            running = self._handle_events()
            self._update(dt_ms)
            self._draw()
        pygame.quit()
