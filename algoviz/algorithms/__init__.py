from .bubble import bubble_sort_steps
from .insertion import insertion_sort_steps
from .selection import selection_sort_steps

ALGORITHMS = {
    "Bubble Sort": bubble_sort_steps,
    "Selection Sort": selection_sort_steps,
    "Insertion Sort": insertion_sort_steps,
}
