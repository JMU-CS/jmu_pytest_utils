from jmu_pytest_utils.common import assert_pep8
from jmu_pytest_utils.decorators import required, weight
from pytest import raises

from game.card import RANKS, SUITS, Card

FILENAME = "../game/card.py"


@required()
def test_globals():
    assert RANKS == [
        None, "Ace", "2", "3", "4", "5", "6", "7",
        "8", "9", "10", "Jack", "Queen", "King"
    ]
    assert SUITS == [
        "Clubs", "Diamonds", "Hearts", "Spades"
    ]


@weight(1)
def test_pep8():
    """PEP 8: card.py"""
    assert_pep8(FILENAME)


@weight(1)
def test_card_int():
    card = Card(1, 2)
    assert card.rank == 1, "incorrect rank"
    assert card.suit == 2, "incorrect suit"
    card = Card(2, 3)
    assert card.rank == 2, "incorrect rank"
    assert card.suit == 3, "incorrect suit"


@weight(1)
def test_card_str():
    card = Card("Ace", "Clubs")
    assert card.rank == 1, "incorrect rank"
    assert card.suit == 0, "incorrect suit"
    card = Card("8", "Diamonds")
    assert card.rank == 8, "incorrect rank"
    assert card.suit == 1, "incorrect suit"


@weight(1)
def test_invalid():
    with raises(ValueError, match="invalid rank: 0"):
        Card(0, 1)
    with raises(ValueError, match="invalid suit: 4"):
        Card(3, 4)
    with raises(ValueError):
        Card("1", "Hearts")
    with raises(ValueError):
        Card("Ace", "Bacon")


@weight(1)
def test_repr():
    assert repr(Card(8, 0)) == "Card(8, 0)"
    assert repr(Card(9, 1)) == "Card(9, 1)"
    assert repr(Card(10, 2)) == "Card(10, 2)"
    assert repr(Card(11, 3)) == "Card(11, 3)"


@weight(1)
def test_str():
    assert str(Card(8, 0)) == "8 of Clubs"
    assert str(Card(9, 1)) == "9 of Diamonds"
    assert str(Card(10, 2)) == "10 of Hearts"
    assert str(Card(11, 3)) == "Jack of Spades"


@weight(1)
def test_color():
    assert Card(8, 0).color() == "black"
    assert Card(8, 1).color() == "red"
    assert Card(8, 2).color() == "red"
    assert Card(8, 3).color() == "black"


@weight(1)
def test_position():
    index = 0
    for suit in range(0, 3):
        for rank in range(1, 14):
            card = Card(rank, suit)
            assert card.position() == index
            index += 1
