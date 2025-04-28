import pytest
import logging
from chess.board import ChessBoard
from chess.pieces import Coordinate, PieceColor


def test_validate_raises_for_duplicate_coordinates(dummy_piece_class, logger) -> None:
    """Ensure validate() raises when two pieces share the same coordinate."""
    coord = Coordinate("A", 1)
    p1 = dummy_piece_class(coord, PieceColor.WHITE)
    p2 = dummy_piece_class(coord, PieceColor.BLACK)
    with pytest.raises(ValueError) as excinfo:
        ChessBoard(pieces=[p1, p2], board_size=8, logger=logger)
    assert "input coordinates must be unique" in str(excinfo.value)


def test_empty_board_property_returns_correct_and_cached(logger) -> None:
    """_empty_board must return an N×N grid of '_' on every access."""
    size = 3
    board = ChessBoard(pieces=[], board_size=size, logger=logger)
    expected = [["_"] * size for _ in range(size)]

    # first access
    grid1 = board._empty_board
    assert grid1 == expected

    # second access still returns the same pattern
    grid2 = board._empty_board
    assert grid2 == expected

    assert grid1 == grid2


def test_populate_board_places_emojis_correctly(create_piece_at_index, logger) -> None:
    """_populate_board should place each piece's emoji at its coordinate."""
    size = 2
    p1 = create_piece_at_index(0, 0, size)
    p2 = create_piece_at_index(1, 1, size)
    board = ChessBoard(pieces=[p1, p2], board_size=size, logger=logger)
    assert board._populate_board() == [
        ["D", "_"],
        ["_", "D"],
    ]


def test_render_logs_board(create_piece_at_index, caplog, logger) -> None:
    """render() must log the intro message and the formatted grid."""
    caplog.set_level(logging.INFO)
    size = 2
    p1 = create_piece_at_index(0, 0, size)
    p2 = create_piece_at_index(1, 1, size)
    board = ChessBoard(pieces=[p1, p2], board_size=size, logger=logger)

    board.render()

    assert any(
        "Rendering the current state of board" in rec.message for rec in caplog.records
    )

    expected = "\nD  _\n_  D\n"
    assert any(rec.message.strip() == expected.strip() for rec in caplog.records)
