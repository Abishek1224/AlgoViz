from typing import Generator, List

from algoviz.models import StepEvent


def bubble_sort_steps(arr: List[int]) -> Generator[StepEvent, None, None]:
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            yield StepEvent("compare", (j, j + 1))
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                yield StepEvent("swap", (j, j + 1))
        yield StepEvent("mark_sorted", (n - i - 1, n - i - 1))
        if not swapped:
            for k in range(0, n - i - 1):
                yield StepEvent("mark_sorted", (k, k))
            break
    yield StepEvent("done", (-1, -1))
