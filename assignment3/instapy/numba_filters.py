"""numba-optimized filters"""
from numba import jit
import numpy as np


@jit(nopython=True)
def numba_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)
    # iterate through the pixels, and apply the grayscale transform

    gray = np.clip(
        image[:, :, 0] * 0.21 + image[:, :, 1] * 0.72 + image[:, :, 2] * 0.07, 0, 255
    )
    gray_image[:, :, 0] = gray
    gray_image[:, :, 1] = gray
    gray_image[:, :, 2] = gray

    gray_image = gray_image.astype("uint8")

    return gray_image


@jit(nopython=True)
def numba_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.zeros_like(image)
    sepia_matrix = np.array(
        [
            [0.393, 0.769, 0.189],  # red
            [0.349, 0.686, 0.168],  # green
            [0.272, 0.534, 0.131],  # blue
        ]
    )
    # Iterate through the pixels
    # applying the sepia matrix
    for i in range(3):
        sepia_image[:, :, i] = np.clip(
            (
                image[:, :, 0] * sepia_matrix[i, 0]
                + image[:, :, 1] * sepia_matrix[i, 1]
                + image[:, :, 2] * sepia_matrix[i, 2]
            ),
            0,
            255,
        )

    sepia_image = sepia_image.astype("uint8")
    # print(sepia_image)

    # Return image
    # don't forget to make sure it's the right type!
    return sepia_image
