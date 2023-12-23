"""numpy implementation of image filters"""

from typing import Optional
import numpy as np


def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    # Hint: use numpy slicing in order to have fast vectorized code

    gray = image[:, :, 0] * 0.21 + image[:, :, 1] * 0.72 + image[:, :, 2] * 0.07
    gray_image = np.empty_like(image)
    gray_image[:, :, 0] = gray
    gray_image[:, :, 1] = gray
    gray_image[:, :, 2] = gray

    # Return image (make sure it's the right type!)
    gray_image = gray_image.astype("uint8")

    return gray_image


def numpy_color2sepia(image: np.array, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia filter to apply (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
    you may ignore it for Task 9)

    Returns:
        np.array: sepia_image
    """

    if not 0 <= k <= 1:
        # validate k (optional)
        raise ValueError(f"k must be between [0-1], got {k=}")

    identity_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    # define sepia matrix (optional: with `k` tuning parameter for bonus task 13)
    sepia_matrix = np.array(
        [
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131],
        ]
    )
    tuned_matrix = k * (sepia_matrix - identity_matrix) + identity_matrix

    # HINT: For version without adaptive sepia filter, use the same matrix as in the pure python implementation
    # use Einstein sum to apply pixel transform matrix

    # Used einsum, but found matmul was faster
    # sepia_image = np.minimum(np.einsum('ijk,sk->ijs', image, sepia_matrix), 255)

    # Apply the matrix filter
    sepia_image = np.minimum(image @ tuned_matrix.transpose(), 255)

    # Check which entries have a value greater than 255 and set it to 255 since we can not display values bigger than 255
    sepia_image = sepia_image.astype("uint8")

    # Return image (make sure it's the right type!)
    return sepia_image
