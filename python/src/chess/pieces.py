from abc import ABC, abstractmethod
from enum import Enum

from chess.move import MoveDirection


def get_available_files(board_size: int) -> list:
    if not (1 <= board_size <= 26):
        raise ValueError("n must be between 1 and 26, inclusive.")
    return [chr(i).upper() for i in range(ord('a'), ord('a') + board_size)]

class Coordinate:
    def __init__(self, file: str, rank: int, board_size: int = 8) -> None:
        self.board_size = board_size
        self.available_files = get_available_files(board_size)
        self.file = file.upper()
        self.rank = rank

        if self.file not in self.available_files:
            raise ValueError(f"file: {file} must be between a and {self.available_files[-1]}, inclusive.")
        if self.rank < 1 or rank > board_size:
            raise ValueError(f"rank: {rank} must be between 1 and {board_size}, inclusive.")

    @classmethod
    def from_indexes(cls, file_index: int, rank_index: int, board_size: int = 8):
        files = get_available_files(board_size)
        if not (0 <= file_index < board_size):
            raise ValueError(f"file_index: {file_index} must be between 0 and {board_size-1}")
        if not (0 <= rank_index < board_size):
            raise ValueError(f"rank_index: {rank_index} must be between 0 and {board_size-1}")

        file = files[file_index]
        rank = board_size - rank_index
        return cls(file, rank, board_size=board_size)

    def __str__(self) -> str:
        return f"{self.file}{self.rank}"

    def __eq__(self, other):
        if not isinstance(other, Coordinate):
            return NotImplemented
        return (self.file, self.rank, self.board_size) == (other.file, other.rank, other.board_size)

    def __hash__(self):
        return hash((self.file, self.rank, self.board_size))

    def file_index(self):
        return self.available_files.index(self.file)

    def rank_index(self):
        return self.board_size - self.rank

class PieceColor(Enum):
    WHITE = "White"
    BLACK = "Black"

class ChessPiece(ABC):

    def __init__(self, coordinate: Coordinate, color: PieceColor) -> None:
        self.color = color
        self.coordinate: Coordinate = coordinate

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the chess piece."""

    @property
    @abstractmethod
    def emoji(self) -> str:
        """Emoji of the chess piece."""

    @abstractmethod
    def can_capture(self, target_coordinate: Coordinate) -> bool:
        """Returns True if the piece (self) can capture the target coordinate."""

    def __str__(self) -> str:
        return f"{self.color.value} {self.name}"


class Rook(ChessPiece):
    def __init__(self, coordinate: Coordinate, color: PieceColor) -> None:
        super().__init__(coordinate, color)

    @property
    def name(self) -> str:
        return "Rook"

    @property
    def emoji(self) -> str:
        if self.color == PieceColor.WHITE:
            return "\u2656"
        else:
            return "\u265C"

    def can_capture(self, target_coordinate: Coordinate) -> bool:
        return self.coordinate.file == target_coordinate.file or self.coordinate.rank == target_coordinate.rank

    def move(self, direction: MoveDirection, spaces: int, board_size: int) -> None:
        file_idx = self.coordinate.file_index()
        rank_idx = self.coordinate.rank_index()

        if direction == MoveDirection.UP:
            new_rank_idx = (rank_idx - spaces) % board_size
            self.coordinate = Coordinate.from_indexes(file_idx, new_rank_idx, board_size)

        elif direction == MoveDirection.RIGHT:
            new_file_idx = (file_idx + spaces) % board_size
            self.coordinate = Coordinate.from_indexes(new_file_idx, rank_idx, board_size)


class Bishop(ChessPiece):
    def __init__(self, coordinate: Coordinate, color: PieceColor) -> None:
        super().__init__(coordinate, color)

    @property
    def name(self) -> str:
        return "Bishop"

    @property
    def emoji(self) -> str:
        if self.color == PieceColor.WHITE:
            return "\u2657"
        else:
            return "\u265D"

    def can_capture(self, target_coordinate: Coordinate) -> bool:
        return abs(self.coordinate.file_index() - target_coordinate.file_index()) == abs(self.coordinate.rank_index() - target_coordinate.rank_index())


