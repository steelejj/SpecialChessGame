import pytest
from unittest.mock import MagicMock, patch

from chess.move import toss_coin, roll_dice, MoveDirection


def test_toss_coin_heads() -> None:
    """toss_coin returns UP when random.choice returns True."""
    mock_choice = MagicMock(return_value=True)
    with patch('chess.move.random.choice', mock_choice):
        result = toss_coin()
    assert result == MoveDirection.UP
    mock_choice.assert_called_once_with([True, False])


def test_toss_coin_tails() -> None:
    """toss_coin returns RIGHT when random.choice returns False."""
    mock_choice = MagicMock(return_value=False)
    with patch('chess.move.random.choice', mock_choice):
        result = toss_coin()
    assert result == MoveDirection.RIGHT
    mock_choice.assert_called_once_with([True, False])


@pytest.mark.parametrize("stubbed", [1, 3, 6])
def test_roll_dice_stubbed(stubbed: int) -> None:
    """roll_dice returns the exact value from random.randint."""
    mock_randint = MagicMock(return_value=stubbed)
    with patch('chess.move.random.randint', mock_randint):
        result = roll_dice()
    assert result == stubbed
    mock_randint.assert_called_once_with(1, 6)


def test_roll_dice_range() -> None:
    """roll_dice returns an integer between 1 and 6 when unmocked."""
    result = roll_dice()
    assert isinstance(result, int)
    assert 1 <= result <= 6
