from typing import Generator, List

from algoviz.models import StepEvent


def selection_sort_steps(arr: List[int]) -> Generator[StepEvent, None, None]:
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield StepEvent("compare", (min_idx, j))
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield StepEvent("swap", (i, min_idx))
        yield StepEvent("mark_sorted", (i, i))
    yield StepEvent("done", (-1, -1))
