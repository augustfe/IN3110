from instapy.python_filters import python_color2gray, python_color2sepia
from PIL import Image
import numpy as np


def test_color2gray(image):
    # run color2gray
    result = python_color2gray(image)
    # check that the result has the right shape, type
    assert result.shape == image.shape
    # assert uniform r,g,b values
    assert np.all([result[:, :, 0], result[:, :, 1]])
    assert np.all([result[:, :, 1], result[:, :, 2]])


def test_color2sepia(image):
    # run color2sepia
    result = python_color2sepia(image)
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
    assert np.all([image[0, 0] @ sepia_matrix.transpose(), result[0, 0]])
    assert np.all([image[10, 36] @ sepia_matrix.transpose(), result[10, 36]])
    assert np.all([image[55, 45] @ sepia_matrix.transpose(), result[55, 45]])
    assert np.all([image[:, :] @ sepia_matrix.transpose(), result[:, :]])
    # according to the sepia matrix


if __name__ == "__main__":
    image = np.asarray(Image.open("rain.jpg"))
    test_color2gray(image)
    test_color2sepia(image)
