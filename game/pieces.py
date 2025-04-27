from abc import ABC, abstractmethod
from enum import Enum

from game.move import MoveDirection


def get_available_files(n: int) -> list:
    if not (1 <= n <= 26):
        raise ValueError("n must be between 1 and 26, inclusive.")
    return [chr(i).upper() for i in range(ord('a'), ord('a') + n)]

class Coordinate:
    def __init__(self, file: str, rank: int, board_size: int = 8):
        self.board_size = board_size
        self.available_files = get_available_files(board_size)
        self.file = file.upper()
        self.rank = rank

        if self.file not in self.available_files:
            raise ValueError(f"file: {file} must be between a and {self.available_files[-1]}, inclusive.")
        if self.rank < 1 or rank > board_size:
            raise ValueError(f"rank: {rank} must be between 1 and {board_size}, inclusive.")

    def __str__(self):
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

    def __init__(self, coordinate: Coordinate, color: PieceColor):
        self.color = color
        self.coordinate: Coordinate = coordinate

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
    def can_capture(self, target_coordinate: Coordinate) -> bool:
        """Returns True if the piece (self) can capture the target coordinate"""
        pass

    def __str__(self):
        return f"{self.color.value} {self.name}"


class Rook(ChessPiece):
    def __init__(self, coordinate: Coordinate, color: PieceColor):
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

    def move(self, direction: MoveDirection, spaces: int, board_size: int) -> ChessPiece:
        if direction == MoveDirection.UP:
            new_rank = self.coordinate.rank + spaces
            if new_rank > board_size:
                new_rank = new_rank - board_size
            self.coordinate.rank = new_rank
        elif direction == MoveDirection.RIGHT:



class Bishop(ChessPiece):
    def __init__(self, coordinate: Coordinate, color: PieceColor):
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
        return abs(self.coordinate.file_index() - target_coordinate.file_index()) == abs(self.coordinate.rank - target_coordinate.rank)


