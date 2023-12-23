from instapy.numba_filters import numba_color2gray, numba_color2sepia

import numpy.testing as nt
import numpy as np
from PIL import Image


def test_color2gray(image, reference_gray):
    # run color2gray
    result = numba_color2gray(image)
    # check that the result has the right shape, type
    assert result.shape == image.shape
    assert isinstance(result, type(image))
    # assert uniform r,g,b values
    assert np.all([result[:, :, 0], result[:, :, 1]])
    assert np.all([result[:, :, 1], result[:, :, 2]])


def test_color2sepia(image, reference_sepia):
    # run color2sepia
    result = numba_color2sepia(image)
    # check that the result has the right shape, type
    assert result.shape == image.shape
    # verify some individual pixel samples
    sepia_matrix = np.array(
        [
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131],
        ]
    )
    nt.assert_allclose(
        np.clip(image[0, 0] @ sepia_matrix.transpose(), 0, 255), result[0, 0], atol=1.5
    )
    nt.assert_allclose(
        np.clip(image[10, 36] @ sepia_matrix.transpose(), 0, 255),
        result[10, 36],
        atol=1.5,
    )
    nt.assert_allclose(
        np.clip(image[55, 45] @ sepia_matrix.transpose(), 0, 255),
        result[55, 45],
        atol=1.5,
    )
    nt.assert_allclose(
        np.clip(image[:, :] @ sepia_matrix.transpose(), 0, 255), result[:, :], atol=1.5
    )
    # according to the sepia matrix
