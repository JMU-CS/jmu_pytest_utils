"""Define constants and class for playing cards."""

RANKS = [
    None, "Ace", "2", "3", "4", "5", "6", "7",
    "8", "9", "10", "Jack", "Queen", "King"
]

SUITS = [
    "Clubs", "Diamonds", "Hearts", "Spades"
]


class Card():
    """A standard (French) playing card.

    Attributes:
        rank (int): The card's rank (index in the RANKS list).
        suit (int): The card's suit (index in the SUITS list).
    """

    def __init__(self, rank, suit):
        """Construct a card with given values.

        If integers are passed, they correspond to indexes in
        the RANKS and SUITS lists. If strings are passed, they
        correspond to values in the RANKS and SUITS lists.

        Args:
            rank (int or str): The card's rank.
            suit (int or str): The card's suit.

        Raises:
            ValueError: if the rank or suit is invalid
        """
        # Validate the rank
        if isinstance(rank, int):
            if rank < 1 or rank > 13:
                raise ValueError(f"invalid rank: {rank}")
            self.rank = rank
        else:
            self.rank = RANKS.index(rank)
        # Validate the suit
        if isinstance(suit, int):
            if suit < 0 or suit > 3:
                raise ValueError(f"invalid suit: {suit}")
            self.suit = suit
        else:
            self.suit = SUITS.index(suit)

    def __repr__(self):
        return f"Card({self.rank}, {self.suit})"

    def __str__(self):
        return f"{RANKS[self.rank]} of {SUITS[self.suit]}"

    def color(self):
        """Get the card's color (black or red)."""
        if self.suit == 0 or self.suit == 3:
            return "black"
        return "red"

    def position(self):
        """Get the card's index in a sorted deck of 52 cards."""
        return self.suit*13 + self.rank - 1
