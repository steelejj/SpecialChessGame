import logging
import pytest
from chess.pieces import ChessPiece, Coordinate, PieceColor


class DummyPiece(ChessPiece):
    """Generic dummy piece with configurable emoji and capture result."""

    def __init__(
        self,
        coordinate: Coordinate,
        color: PieceColor,
        emoji: str = "D",
        can_capture_result: bool = False,
    ) -> None:
        super().__init__(coordinate, color)
        self._emoji = emoji
        self._can_capture = can_capture_result

    @property
    def name(self) -> str:
        return "Dummy"

    @property
    def emoji(self) -> str:
        return self._emoji

    def can_capture(self, target_coordinate: Coordinate) -> bool:
        return self._can_capture


@pytest.fixture
def dummy_piece_class():
    """Provide the generic DummyPiece class."""
    return DummyPiece


@pytest.fixture
def create_piece_at_index(dummy_piece_class):
    """Build a DummyPiece at zero-based indexes on an N×N board."""

    def _create(
        file_idx: int,
        rank_idx: int,
        board_size: int = 3,
        color: PieceColor = PieceColor.WHITE,
        emoji: str = "D",
        can_capture: bool = False,
    ):
        coord = Coordinate.from_indexes(file_idx, rank_idx, board_size)
        return dummy_piece_class(
            coord, color, emoji=emoji, can_capture_result=can_capture
        )

    return _create


@pytest.fixture
def logger():
    """Provide a default stdlib logger."""
    return logging.getLogger(__name__)
