from jmu_pytest_utils.common import assert_pep8
from jmu_pytest_utils.decorators import weight

from game.card import Card
from util.score import casino

FILENAME = "../util/score.py"


@weight(1)
def test_pep8():
    """PEP 8: score.py"""
    assert_pep8(FILENAME)


@weight(1)
def test_casino():
    assert casino(Card(1, 0)) == 1
    assert casino(Card(1, 3)) == 1
    assert casino(Card(2, 0)) == 5
    assert casino(Card(2, 3)) == 5
    assert casino(Card(9, 1)) == 0
    assert casino(Card(9, 2)) == 0
    assert casino(Card(10, 1)) == 10
    assert casino(Card(10, 2)) == 10
