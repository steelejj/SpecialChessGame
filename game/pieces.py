from abc import ABC, abstractmethod
from enum import Enum


def get_alphabet_list(n: int) -> list:
    if not (1 <= n <= 26):
        raise ValueError("n must be between 1 and 26, inclusive.")
    return [chr(i) for i in range(ord('a'), ord('a') + n)]

class Coordinate:
    def __init__(self, file: str, rank: int, board_size: int = 8):
        self.board_size = board_size
        self.available_files = get_alphabet_list(board_size)

        if file.lower() not in self.available_files:
            raise ValueError(f"file: {file} must be between a and {self.available_files[-1]}, inclusive.")
        if rank < 0 or rank > board_size:
            raise ValueError(f"rank: {rank} must be between 0 and {board_size}, inclusive.")

        self.file = file
        self.rank = rank

    def file_index(self):
        return self.available_files.index(self.file)

    def rank_index(self):
        return self.board_size - self.rank

class PieceColor(Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"

class ChessPiece(ABC):

    def __init__(self, color: PieceColor):
        self.color = color

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the chess piece"""
        pass

    @property
    @abstractmethod
    def emoji(self) -> str:
        """Emoji of the chess piece"""
        pass

    @abstractmethod
    def can_capture(self, source_coordinate: Coordinate, target_coordinate: Coordinate) -> bool:
        """Returns True if the source cardinate (self) can capture the target coordinate"""
        pass


class Rook(ChessPiece):
    def __init__(self, color: PieceColor):
        super().__init__(color)

    @property
    def name(self) -> str:
        return "Rook"

    @property
    def emoji(self) -> str:
        return "\u2656"

    def can_capture(self, source_coordinate: Coordinate, target_coordinate: Coordinate) -> bool:
        return source_coordinate.file == target_coordinate.file or source_coordinate.rank == target_coordinate.rank


class Bishop(ChessPiece):
    def __init__(self, color: PieceColor):
        super().__init__(color)

    @property
    def name(self) -> str:
        return "Bishop"

    @property
    def emoji(self) -> str:
        return "\u265D"

    def can_capture(self, source_coordinate: Coordinate, target_coordinate: Coordinate) -> bool:
        return abs(source_coordinate.file_index() - target_coordinate.file_index()) == abs(source_coordinate.rank - target_coordinate.rank)


