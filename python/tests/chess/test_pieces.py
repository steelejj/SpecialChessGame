# tests/test_pieces.py

import pytest
from enum import Enum

from chess.pieces import (
    get_available_files,
    Coordinate,
    PieceColor,
    ChessPiece,
    Rook,
    Bishop,
)
from chess.move import MoveDirection


def test_get_available_files_valid() -> None:
    """get_available_files should return correct letters for valid sizes."""
    assert get_available_files(1) == ["A"]
    assert get_available_files(3) == ["A", "B", "C"]
    full = get_available_files(26)
    assert full[0] == "A" and full[-1] == "Z" and len(full) == 26


@pytest.mark.parametrize("invalid_size", [0, -5, 27, 100])
def test_get_available_files_invalid(invalid_size: int) -> None:
    """get_available_files should raise ValueError for out-of-range sizes."""
    with pytest.raises(ValueError):
        get_available_files(invalid_size)


def test_coordinate_init_and_str() -> None:
    """Coordinate should normalize file to uppercase and __str__ produce 'A1'."""
    coord = Coordinate("a", 1, board_size=8)
    assert coord.file == "A"
    assert coord.rank == 1
    assert str(coord) == "A1"


@pytest.mark.parametrize("file,rank", [
    ("?", 1),
    ("A", 0),
    ("A", 9),
])
def test_coordinate_invalid_file_or_rank(file: str, rank: int) -> None:
    """Coordinate __init__ should reject invalid file letters or rank numbers."""
    with pytest.raises(ValueError):
        Coordinate(file, rank, board_size=8)


def test_coordinate_from_indexes_valid() -> None:
    """from_indexes should map (0,7)->A1 and (7,0)->H8 on an 8×8 board."""
    c1 = Coordinate.from_indexes(0, 7, board_size=8)
    c2 = Coordinate.from_indexes(7, 0, board_size=8)
    assert str(c1) == "A1"
    assert str(c2) == "H8"


@pytest.mark.parametrize("fi,ri", [(-1,0), (0,-1), (8,0), (0,8)])
def test_coordinate_from_indexes_invalid(fi: int, ri: int) -> None:
    """from_indexes should reject indexes outside [0, board_size)."""
    with pytest.raises(ValueError):
        Coordinate.from_indexes(fi, ri, board_size=8)


def test_coordinate_equality_and_hash() -> None:
    """Coordinates with same file, rank, size should be equal and hash identically."""
    c1 = Coordinate("B", 2, board_size=5)
    c2 = Coordinate.from_indexes(1, 3, board_size=5)  # 5-3=2 → rank 2
    assert c1 == c2
    assert hash(c1) == hash(c2)
    assert not (c1 != c2)


def test_file_and_rank_index() -> None:
    """file_index and rank_index should return correct zero-based positions."""
    coord = Coordinate("C", 3, board_size=5)
    assert coord.file_index() == 2
    assert coord.rank_index() == 5 - 3


def test_piececolor_enum() -> None:
    """PieceColor should have WHITE and BLACK with correct values."""
    assert PieceColor.WHITE.value == "White"
    assert PieceColor.BLACK.value == "Black"
    assert list(PieceColor) == [PieceColor.WHITE, PieceColor.BLACK]


def test_chesspiece_is_abstract() -> None:
    """ChessPiece cannot be instantiated directly due to abstract methods."""
    with pytest.raises(TypeError):
        ChessPiece(Coordinate("A", 1), PieceColor.WHITE)  # type: ignore


class DummyPiece(ChessPiece):
    """Concrete subclass for testing ChessPiece behavior."""

    def __init__(self, coordinate: Coordinate, color: PieceColor) -> None:
        super().__init__(coordinate, color)

    @property
    def name(self) -> str:
        return "Dummy"

    @property
    def emoji(self) -> str:
        return "X"

    def can_capture(self, target_coordinate: Coordinate) -> bool:
        return True


def test_dummy_piece_str_and_capture() -> None:
    """DummyPiece should implement __str__ and can_capture correctly."""
    coord = Coordinate("D", 4, board_size=8)
    p = DummyPiece(coord, PieceColor.BLACK)
    assert str(p) == "Black Dummy"
    assert p.can_capture(Coordinate("E", 5, board_size=8))


@pytest.mark.parametrize(
    "start,direction,spaces,expected",
    [
        (("A", 1), MoveDirection.UP, 1, "A2"),
        (("H", 8), MoveDirection.UP, 2, "H2"),
        (("A", 1), MoveDirection.RIGHT, 3, "D1"),
        (("G", 5), MoveDirection.RIGHT, 5, "D5"),
    ],
)
def test_rook_move_and_capture(
    start: tuple[str, int],
    direction: MoveDirection,
    spaces: int,
    expected: str,
) -> None:
    """Rook.move should wrap correctly and post-move can_capture should be True."""
    coord = Coordinate(start[0], start[1], board_size=8)
    rook = Rook(coord, PieceColor.WHITE)

    # perform the move and check wrapping
    rook.move(direction=direction, spaces=spaces, board_size=8)
    assert str(rook.coordinate) == expected

    # after moving, rook should always be able to capture its own square
    assert rook.can_capture(rook.coordinate)


@pytest.mark.parametrize(
    "start,target,expected",
    [
        (("C", 1), ("F", 4), True),
        (("A", 1), ("H", 8), True),
        (("D", 5), ("E", 7), False),
        (("E", 6), ("E", 5), False),
    ],
)
def test_bishop_capture(
    start: tuple[str, int],
    target: tuple[str, int],
    expected: bool,
) -> None:
    """Bishop.can_capture should only allow diagonal captures."""
    b = Bishop(Coordinate(start[0], start[1], board_size=8), PieceColor.BLACK)
    result = b.can_capture(Coordinate(target[0], target[1], board_size=8))
    assert result is expected
