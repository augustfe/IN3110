from instapy.numpy_filters import numpy_color2gray, numpy_color2sepia

import numpy.testing as nt
from PIL import Image
import numpy as np


def test_color2gray(image, reference_gray):
    result = numpy_color2gray(image)
    # check that the result has the right shape, type
    assert result.shape == image.shape
    # assert uniform r,g,b values
    nt.assert_allclose(result[:,:,0], result[:,:,1])
    nt.assert_allclose(result[:,:,1], result[:,:,2])
    nt.assert_allclose(result, reference_gray)


def test_color2sepia(image, reference_sepia):
    # run color2sepia
    result = numpy_color2sepia(image)
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
    nt.assert_allclose(result, reference_sepia)


if __name__ == "__main__":
    image = np.asarray(Image.open("rain.jpg"))
    test_color2gray(image, 1)
    test_color2sepia(image, 1)
