"""
Timing our filter implementations.

Can be executed as `python3 -m instapy.timing > timing-report.txt`

For Task 6.
"""
import time
import instapy
from . import io
from typing import Callable
import numpy as np
from PIL import Image


def time_one(filter_function: Callable, *arguments, calls: int = 3) -> float:
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    t0 = time.perf_counter()
    # run the filter function `calls` times
    for j in range(calls):
        filter_function(*arguments)
    t1 = time.perf_counter()
    # return the _average_ time of one call
    return (t1 - t0) / calls


def make_reports(filename: str = "test/rain.jpg", calls: int = 3):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
    """

    # load the image
    image = np.asarray(Image.open(filename))

    # print the image name, width, height
    print(f"Timing performed using {filename}: {image.shape[1]}x{image.shape[0]}")

    # iterate through the filters
    filter_names = ["color2gray", "color2sepia"]
    for filter_name in filter_names:
        # get the reference filter function
        reference_filter = instapy.get_filter(filter_name, "python")
        # time the reference implementation
        reference_time = time_one(reference_filter, image)
        print(
            f"\nReference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=})"
        )

        # iterate through the implementations
        implementations = ["numpy", "numba"]
        for implementation in implementations:
            filter = instapy.get_filter(filter_name, implementation)
            # time the filter

            first_time = time_one(filter, image, calls=1)
            filter_time = time_one(filter, image, calls=calls)
            # compare the reference time to the optimized time

            speedup = reference_time / filter_time
            print(
                f"Timing: {implementation} {filter_name}: first call: {first_time:.3}s, average after: {filter_time:.3}s ({speedup=:.2f}x)"
            )


if __name__ == "__main__":
    # run as `python -m instapy.timing`
    make_reports()
