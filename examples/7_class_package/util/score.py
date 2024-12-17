"""Utility functions for card games."""


def casino(card):
    """Get a card's value in the game of Casino.

    Args:
        card (Card): The card to score.

    Returns:
        int: How many points the card is worth.
    """
    if card.color() == "black":
        if card.rank == 2:
            value = 5
        else:
            value = 1
    else:
        if card.rank == 10:
            value = 10
        else:
            value = 0
    return value
