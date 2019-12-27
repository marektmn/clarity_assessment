import pytest
from parser import convert_adjust_time, most_frequent, finite_parser, infinite_parser


@pytest.mark.parametrize("test_input,expected",
                    [([1, 2, 3], 1), (['A', 'A', 'B'], 'A'),
                     (['A', 'A', 'B', 'B', 'C'], 'A'),
                     pytest.param([], ValueError, marks=pytest.mark.xfail)])
def test_most_frequent(test_input, expected):
    assert most_frequent(test_input) == expected


@pytest.mark.parametrize("test_input1, test_input2, test_input3, expected",
                         [('2019-08-13T08:28:31+00:00', 0, False, 1565684911),
                          ('2019-08-13T08:28:31Z', 0, False, 1565684911),
                          ('1565647212986', 0, True, 1565647212),
                          ('2019-08-13T08:28:31+00:00', 5, False, 1565685211),
                          ('1565647212986', -5, True, 1565646912),
                          ])
def test_iso_to_unixtimestamp(test_input1, test_input2, test_input3, expected):
    assert convert_adjust_time(test_input1, test_input2, test_input3) == expected


def test_infinite_parser():
    pass


def test_finite_parser():
    pass
