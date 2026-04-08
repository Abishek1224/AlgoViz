from typing import Generator, List

from algoviz.models import StepEvent


def insertion_sort_steps(arr: List[int]) -> Generator[StepEvent, None, None]:
    n = len(arr)
    for i in range(1, n):
        j = i
        while j > 0:
            yield StepEvent("compare", (j - 1, j))
            if arr[j - 1] <= arr[j]:
                break
            arr[j - 1], arr[j] = arr[j], arr[j - 1]
            yield StepEvent("swap", (j - 1, j))
            j -= 1
        yield StepEvent("mark_sorted", (i, i))
    yield StepEvent("mark_sorted", (0, 0))
    yield StepEvent("done", (-1, -1))
