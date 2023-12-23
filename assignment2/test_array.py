"""
Tests for our array class
"""

from array_class import Array
import pytest

# 1D tests (Task 4)


def test_str_1d():
    a = Array((4,), 1, 5, 1, 2)
    assert str(a) == '[1, 5, 1, 2]'


def test_add_1d():
    a = Array((4,), 1, 5, 1, 2)
    b = Array((4,), 1, 2, 3, 4)
    c = Array((4,), True, True, False, False)
    assert str(a+4) == '[5, 9, 5, 6]'
    assert str(4+a) == '[5, 9, 5, 6]'
    assert str(a+b) == '[2, 7, 4, 6]'
    assert str(a+4.5) == '[5.5, 9.5, 5.5, 6.5]'
    with pytest.raises(TypeError):
        a + c
    with pytest.raises(TypeError):
        a + True
    with pytest.raises(ValueError):
        a + Array((3,), 1, 2, 3)



def test_sub_1d():
    a = Array((4,), 1, 5, 1, 2)
    b = Array((4,), 1, 2, 3, 4)
    c = Array((4,), True, True, False, False)
    assert str(a-4) == '[-3, 1, -3, -2]'
    assert str(a-b) == '[0, 3, -2, -2]'
    assert str(4-a) == '[3, -1, 3, 2]'
    with pytest.raises(TypeError):
        a - c
    with pytest.raises(TypeError):
        a - True
    with pytest.raises(ValueError):
        a - Array((3,), 1, 2, 3)



def test_mul_1d():
    a = Array((4,), 1, 5, 1, 2)
    b = Array((4,), 1, 2, 3, 4)
    c = Array((4,), True, True, False, False)
    assert str(a*4) == '[4, 20, 4, 8]'
    assert str(a*b) == '[1, 10, 3, 8]'
    assert str(4*a) == '[4, 20, 4, 8]'
    with pytest.raises(TypeError):
        a * c
    with pytest.raises(TypeError):
        a * True
    with pytest.raises(ValueError):
        a * Array((3,), 1, 2, 3)


def test_eq_1d():
    a = Array((4,), 1, 5, 1, 2)
    b = Array((4,), 1, 2, 3, 4)
    c = Array((4,), 1, 5, 1, 2)
    d = Array((2,), 1, 2)
    assert (a == b) == False
    assert (a == c) == True
    assert (a == d) == False


def test_same_1d():
    a = Array((4,), 1, 5, 1, 2)
    b = Array((4,), 1, 2, 3, 2)
    c = Array((3,), 1, 2, 3)
    assert str(a.is_equal(b)) == '[True, False, False, True]'
    assert str(a.is_equal(1)) == '[True, False, True, False]'
    with pytest.raises(ValueError):
        a.is_equal(c)
    with pytest.raises(TypeError):
        a.is_equal('4')

def test_smallest_1d():
    a = Array((4,), 1, 5, 1, 2)
    assert a.min_element() == 1


def test_mean_1d():
    a = Array((4,), 1, 5, 1, 2)
    assert a.mean_element() == 9/4


# 2D tests (Task 6)


def test_add_2d():
    a = Array((3, 2), 8, 3, 4, 1, 6, 1)
    b = Array((3, 2), 1, 2, 3, 4, 5, 1)
    assert str(a+b) == '[[9, 5], [7, 5], [11, 2]]'
    assert str(a+4) == '[[12, 7], [8, 5], [10, 5]]'
    assert str(4+a) == '[[12, 7], [8, 5], [10, 5]]'
    assert str(a+4.5) == '[[12.5, 7.5], [8.5, 5.5], [10.5, 5.5]]'
    with pytest.raises(TypeError):
        a+True


def test_mult_2d():
    a = Array((3, 2), 8, 3, 4, 1, 6, 1)
    b = Array((3, 2), 1, 2, 3, 4, 5, 1)
    assert str(a*4) == '[[32, 12], [16, 4], [24, 4]]'
    assert str(4*a) == '[[32, 12], [16, 4], [24, 4]]'
    assert str(a*b) == '[[8, 6], [12, 4], [30, 1]]'



def test_same_2d():
    a = Array((3, 2), 8, 3, 4, 1, 6, 1)
    b = Array((3, 2), 1, 2, 3, 4, 5, 1)
    assert str(a.is_equal(b)) == '[[False, False], [False, False], [False, True]]'
    assert str(a.is_equal(1)) == '[[False, False], [False, True], [False, True]]'



def test_mean_2d():
    a = Array((3, 2), 8, 3, 4, 1, 6, 1)
    assert a.mean_element() == 23/6



if __name__ == "__main__":
    """
    Note: Write "pytest" in terminal in the same folder as this file is in to run all tests
    (or run them manually by running this file).
    Make sure to have pytest installed (pip install pytest, or install anaconda).
    """

    # Task 4: 1d tests
    test_str_1d()
    test_add_1d()
    test_sub_1d()
    test_mul_1d()
    test_eq_1d()
    test_mean_1d()
    test_same_1d()
    test_smallest_1d()

    # Task 6: 2d tests
    test_add_2d()
    test_mult_2d()
    test_same_2d()
    test_mean_2d()
