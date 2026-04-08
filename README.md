# AlgoViz - Phase 2 Starter

Python + Pygame interactive algorithm visualization project for BSc IT presentations.

## Included

- Sorting visualizations:
  - Bubble Sort
  - Selection Sort
  - Insertion Sort
- UI controls:
  - Play, Pause, Step, Reset, Shuffle
  - Previous/Next algorithm
  - Speed slider
  - Array size slider
  - Custom input box (`5,1,9,3,...`)
  - Theme toggle (dark/light)
  - Sound toggle (demo-ready switch)
- Learning metrics:
  - Comparisons
  - Swaps
  - Total steps
- Complexity panel (best/average/worst + stability)
- Color highlights:
  - Compare (yellow)
  - Swap (red)
  - Sorted (green)

## Run

1. Install dependencies:
   - `pip install -r requirements.txt`
   - If you still face issues, use Python 3.12/3.13 in a virtual environment.
2. Start app:
   - `python main.py`

### Why this dependency?

- `pygame-ce` is a community edition that stays compatible with newer Python versions.
- It is a drop-in replacement, so your code still uses `import pygame`.

## Presentation Tips

- Show the same shuffled array for different algorithms.
- Use Step mode to explain compare/swap operations.
- Increase speed for full-run demo, then pause at key states.
- Enter your own input list for predictable demos.
