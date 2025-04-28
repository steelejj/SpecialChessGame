import logging
import pytest
from chess.board import ChessBoard
from chess.pieces import ChessPiece, Coordinate, PieceColor


class DummyPiece(ChessPiece):
    """Minimal ChessPiece implementation for testing."""

    def __init__(self, coordinate: Coordinate, color: PieceColor) -> None:
        super().__init__(coordinate, color)

    @property
    def name(self) -> str:
        return "Dummy"

    @property
    def emoji(self) -> str:
        return "D"

    def can_capture(self, target_coordinate: Coordinate) -> bool:
        return False


def create_piece_at_index(
    file_idx: int, rank_idx: int, board_size: int = 3
) -> DummyPiece:
    """Helper: build a DummyPiece at zero-based indexes on an N×N board."""
    coord = Coordinate.from_indexes(file_idx, rank_idx, board_size)
    return DummyPiece(coord, PieceColor.WHITE)


def test_validate_raises_for_duplicate_coordinates() -> None:
    """Ensure validate() raises when two pieces share the same coordinate."""
    coord = Coordinate("A", 1)
    p1 = DummyPiece(coord, PieceColor.WHITE)
    p2 = DummyPiece(coord, PieceColor.BLACK)
    with pytest.raises(ValueError) as excinfo:
        ChessBoard(pieces=[p1, p2], board_size=8, logger=logging.getLogger())
    assert "input coordinates must be unique" in str(excinfo.value)


def test_empty_board_property_returns_correct_and_cached() -> None:
    """_empty_board must return an N×N grid of '_' on every access."""
    size = 3
    board = ChessBoard(pieces=[], board_size=size, logger=logging.getLogger())
    expected = [["_"] * size for _ in range(size)]

    # first access
    grid1 = board._empty_board
    assert grid1 == expected

    # second access still returns the same pattern
    grid2 = board._empty_board
    assert grid2 == expected

    assert grid1 == grid2


def test_populate_board_places_emojis_correctly() -> None:
    """_populate_board should place each piece's emoji at its coordinate."""
    size = 2
    # top-left and bottom-right on a 2×2
    p1 = create_piece_at_index(0, 0, size)
    p2 = create_piece_at_index(1, 1, size)
    board = ChessBoard(pieces=[p1, p2], board_size=size, logger=logging.getLogger())
    assert board._populate_board() == [
        ["D", "_"],
        ["_", "D"],
    ]


def test_render_logs_board(caplog) -> None:
    """render() must log the intro message and the formatted grid."""
    caplog.set_level(logging.INFO)
    size = 2
    p1 = create_piece_at_index(0, 0, size)
    p2 = create_piece_at_index(1, 1, size)
    logger = logging.getLogger("test_render")
    board = ChessBoard(pieces=[p1, p2], board_size=size, logger=logger)

    board.render()

    # Check that the rendering message appears
    assert any(
        "Rendering the current state of board" in rec.message for rec in caplog.records
    )

    # Check that the grid was logged (two spaces between cells)
    expected = "\nD  _\n_  D\n"
    # strip to ignore leading/trailing whitespace
    assert any(rec.message.strip() == expected.strip() for rec in caplog.records)
