"""pure Python implementation of image filters"""

import numpy as np


def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    # iterate through the pixels, and apply the grayscale transform
    gray_image = np.empty_like(image)
    for j, ny in enumerate(image):
        for i, nx in enumerate(ny):
            red, green, blue = nx
            gray = red * 0.21 + green * 0.72 + blue * 0.07
            gray_image[j][i] = [gray, gray, gray]
    gray_image = gray_image.astype("uint8")

    return gray_image


def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image)
    sepia_matrix = [
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131],
    ]
    # Iterate through the pixels
    # applying the sepia matrix
    for j, ny in enumerate(image):
        for i, nx in enumerate(ny):
            for k, row in enumerate(sepia_matrix):
                sepia_image[j][i][k] = min(
                    255, sum([colour * weight for colour, weight in zip(nx, row)])
                )

    sepia_image = sepia_image.astype("uint8")

    # Return image
    # don't forget to make sure it's the right type!
    return sepia_image
