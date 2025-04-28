import pytest
from unittest.mock import MagicMock, patch
from logging import Logger

from chess.game import Game
from chess.pieces import Rook, Bishop
from chess.move import MoveDirection


@pytest.fixture
def logger() -> MagicMock:
    """Fixture providing a MagicMock logger."""
    return MagicMock(spec=Logger)


@pytest.fixture
def rook() -> MagicMock:
    """Fixture for a mock Rook piece."""
    r = MagicMock(spec=Rook)
    r.coordinate = MagicMock()
    return r


@pytest.fixture
def bishop() -> MagicMock:
    """Fixture for a mock Bishop piece."""
    b = MagicMock(spec=Bishop)
    b.coordinate = MagicMock()
    return b


@patch("chess.game.ChessBoard")
@patch("chess.game.roll_dice")
@patch("chess.game.toss_coin")
def test_play_turn_rook_captures_first(
    mock_toss: MagicMock,
    mock_roll: MagicMock,
    mock_board_cls: MagicMock,
    rook: MagicMock,
    bishop: MagicMock,
    logger: MagicMock,
) -> None:
    """If the rook can already capture the bishop, play_turn returns the rook."""
    rook.can_capture.return_value = True

    game = Game(rook=rook, bishop=bishop, logger=logger)
    result = game._play_turn()

    assert result is rook
    rook.can_capture.assert_called_once_with(bishop.coordinate)
    logger.info.assert_called_with(
        f"The rook on {rook.coordinate} can capture the bishop on {bishop.coordinate}."
    )
    mock_toss.assert_not_called()
    mock_roll.assert_not_called()
    rook.move.assert_not_called()


@patch("chess.game.ChessBoard")
@patch("chess.game.roll_dice")
@patch("chess.game.toss_coin")
def test_play_turn_bishop_captures_after_move(
    mock_toss: MagicMock,
    mock_roll: MagicMock,
    mock_board_cls: MagicMock,
    rook: MagicMock,
    bishop: MagicMock,
    logger: MagicMock,
) -> None:
    rook.can_capture.return_value = False
    bishop.can_capture.return_value = True
    mock_toss.return_value = MoveDirection.UP
    mock_roll.side_effect = [2, 3]

    game = Game(rook=rook, bishop=bishop, logger=logger)
    result = game._play_turn()

    assert result is bishop
    mock_toss.assert_called_once()
    assert mock_roll.call_count == 2
    rook.move.assert_called_once_with(
        direction=MoveDirection.UP, spaces=5, board_size=8
    )
    bishop.can_capture.assert_called_once_with(rook.coordinate)
    logger.info.assert_any_call(
        f"The bishop on {bishop.coordinate} can capture the rook on {rook.coordinate}."
    )


@patch("chess.game.ChessBoard")
@patch("chess.game.roll_dice")
@patch("chess.game.toss_coin")
def test_play_turn_no_capture(
    mock_toss: MagicMock,
    mock_roll: MagicMock,
    mock_board_cls: MagicMock,
    rook: MagicMock,
    bishop: MagicMock,
    logger: MagicMock,
) -> None:
    rook.can_capture.return_value = False
    bishop.can_capture.return_value = False
    mock_toss.return_value = MoveDirection.RIGHT
    mock_roll.side_effect = [1, 1]

    game = Game(rook=rook, bishop=bishop, logger=logger)
    result = game._play_turn()

    assert result is None
    rook.move.assert_called_once_with(
        direction=MoveDirection.RIGHT, spaces=2, board_size=8
    )
    bishop.can_capture.assert_called_once_with(rook.coordinate)
    logger.info.assert_any_call(
        f"The bishop on {bishop.coordinate} cannot capture the rook on {rook.coordinate}."
    )


@patch("chess.game.ChessBoard")
def test_play_game_stops_on_capture(
    mock_board_cls: MagicMock,
    rook: MagicMock,
    bishop: MagicMock,
    logger: MagicMock,
) -> None:
    board_instance = MagicMock()
    mock_board_cls.return_value = board_instance

    game = Game(rook=rook, bishop=bishop, logger=logger)
    game._play_turn = MagicMock(side_effect=[None, None, rook])

    winner, turns = game.play_game(number_of_turns=5)

    assert winner is rook
    assert turns == 3
    # initial render + one per turn
    assert board_instance.render.call_count == 4
