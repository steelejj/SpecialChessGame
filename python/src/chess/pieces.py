from abc import ABC, abstractmethod
from enum import Enum

from chess.move import MoveDirection


def get_available_files(board_size: int) -> list:
    """Generate a list of file letters for a chessboard.

    Args:
        board_size (int): Number of files (columns), between 1 and 26 inclusive.

    Returns:
        list: Uppercase letters from 'A' up to the given board size.

    Raises:
        ValueError: If `board_size` is not between 1 and 26 (letters in the alphabet).
    """
    if not (1 <= board_size <= 26):
        raise ValueError("n must be between 1 and 26, inclusive.")
    return [chr(i).upper() for i in range(ord("a"), ord("a") + board_size)]


class Coordinate:
    """Represents a position on the chessboard by file (letter) and rank (number).

    Attributes:
        board_size (int): Size of the board (number of ranks/files).
        available_files (list): Valid file letters for this board size.
        file (str): The file letter (e.g., 'A').
        rank (int): The rank number (1-based).
    """

    def __init__(self, file: str, rank: int, board_size: int = 8) -> None:
        """Initialize a Coordinate from file and rank.

        Args:
            file (str): File letter, case-insensitive.
            rank (int): Rank number, between 1 and `board_size`.
            board_size (int, optional): Size of the board. Defaults to 8.

        Raises:
            ValueError: If file or rank are out of valid range.
        """
        self.board_size = board_size
        self.available_files = get_available_files(board_size)
        self.file = file.upper()
        self.rank = rank

        if self.file not in self.available_files:
            raise ValueError(
                f"file: {file} must be between a and {self.available_files[-1]}, inclusive.",
            )
        if self.rank < 1 or rank > board_size:
            raise ValueError(
                f"rank: {rank} must be between 1 and {board_size}, inclusive.",
            )

    @classmethod
    def from_indexes(cls, file_index: int, rank_index: int, board_size: int = 8):
        """Create a Coordinate from zero-based file and rank indexes.

        Args:
            file_index (int): Zero-based index for file (0 <= file_index < board_size).
            rank_index (int): Zero-based index for rank (0 <= rank_index < board_size).
            board_size (int, optional): Size of the board. Defaults to 8.

        Returns:
            Coordinate: The corresponding Coordinate instance.

        Raises:
            ValueError: If indexes are out of valid range.
        """
        files = get_available_files(board_size)
        if not (0 <= file_index < board_size):
            raise ValueError(
                f"file_index: {file_index} must be between 0 and {board_size-1}",
            )
        if not (0 <= rank_index < board_size):
            raise ValueError(
                f"rank_index: {rank_index} must be between 0 and {board_size-1}",
            )

        file = files[file_index]
        rank = board_size - rank_index
        return cls(file, rank, board_size=board_size)

    def __str__(self) -> str:
        """Return the coordinate in standard notation.

        Returns:
            str: File letter followed by rank number (e.g., 'A1').
        """
        return f"{self.file}{self.rank}"

    def __eq__(self, other):
        """Check equality of two Coordinates.

        Args:
            other (Coordinate): Another Coordinate to compare.

        Returns:
            bool: True if file, rank, and board_size are all equal.
        """
        if not isinstance(other, Coordinate):
            return NotImplemented
        return (self.file, self.rank, self.board_size) == (
            other.file,
            other.rank,
            other.board_size,
        )

    def __hash__(self):
        """Compute a hash based on file, rank, and board_size."""
        return hash((self.file, self.rank, self.board_size))

    def file_index(self):
        """Get zero-based index of the file."""
        return self.available_files.index(self.file)

    def rank_index(self):
        """Get zero-based index of the rank."""
        return self.board_size - self.rank


class PieceColor(Enum):
    """Enumeration of chess piece colors."""

    WHITE = "White"
    BLACK = "Black"


class ChessPiece(ABC):
    """Abstract base class for chess pieces.

    Attributes:
        coordinate (Coordinate): Position of the piece on the board.
        color (PieceColor): Color of the piece.
    """

    def __init__(self, coordinate: Coordinate, color: PieceColor) -> None:
        """Initialize a ChessPiece.

        Args:
            coordinate (Coordinate): Starting position of the piece.
            color (PieceColor): Color of the piece.
        """
        self.color = color
        self.coordinate: Coordinate = coordinate

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the chess piece."""

    @property
    @abstractmethod
    def emoji(self) -> str:
        """Emoji representation of the chess piece."""

    @abstractmethod
    def can_capture(self, target_coordinate: Coordinate) -> bool:
        """Determine if this piece can capture a given coordinate.

        Args:
            target_coordinate (Coordinate): Position to test.

        Returns:
            bool: True if capture is possible, False otherwise.
        """

    def __str__(self) -> str:
        """Return a readable name of the piece, including its color."""
        return f"{self.color.value} {self.name}"


class Rook(ChessPiece):
    """Rook chess piece, moves horizontally or vertically."""

    def __init__(self, coordinate: Coordinate, color: PieceColor) -> None:
        """Initialize a Rook.

        Args:
            coordinate (Coordinate): Starting position.
            color (PieceColor): Piece color.
        """
        super().__init__(coordinate, color)

    @property
    def name(self) -> str:
        """Name of the piece."""
        return "Rook"

    @property
    def emoji(self) -> str:
        """Emoji representation of the rook."""
        if self.color == PieceColor.WHITE:
            return "\u2656"
        else:
            return "\u265c"

    def can_capture(self, target_coordinate: Coordinate) -> bool:
        """Check if the rook can capture at the target coordinate.

        Args:
            target_coordinate (Coordinate): Position to test.

        Returns:
            bool: True if same file or same rank.
        """
        return (
            self.coordinate.file == target_coordinate.file
            or self.coordinate.rank == target_coordinate.rank
        )

    def move(self, direction: MoveDirection, spaces: int, board_size: int) -> None:
        """Move the rook in a given direction by a number of spaces.

        Args:
            direction (MoveDirection): UP or RIGHT.
            spaces (int): Number of spaces to move.
            board_size (int): Size of the board for wrapping.
        """
        file_idx = self.coordinate.file_index()
        rank_idx = self.coordinate.rank_index()

        if direction == MoveDirection.UP:
            new_rank_idx = (rank_idx - spaces) % board_size
            self.coordinate = Coordinate.from_indexes(
                file_idx,
                new_rank_idx,
                board_size,
            )
        elif direction == MoveDirection.RIGHT:
            new_file_idx = (file_idx + spaces) % board_size
            self.coordinate = Coordinate.from_indexes(
                new_file_idx,
                rank_idx,
                board_size,
            )


class Bishop(ChessPiece):
    """Bishop chess piece, moves diagonally."""

    def __init__(self, coordinate: Coordinate, color: PieceColor) -> None:
        """Initialize a Bishop.

        Args:
            coordinate (Coordinate): Starting position.
            color (PieceColor): Piece color.
        """
        super().__init__(coordinate, color)

    @property
    def name(self) -> str:
        """Name of the piece."""
        return "Bishop"

    @property
    def emoji(self) -> str:
        """Emoji representation of the bishop."""
        if self.color == PieceColor.WHITE:
            return "\u2657"
        else:
            return "\u265d"

    def can_capture(self, target_coordinate: Coordinate) -> bool:
        """Check if the bishop can capture at the target coordinate.

        Args:
            target_coordinate (Coordinate): Position to test.

        Returns:
            bool: True if on the same diagonal.
        """
        return abs(
            self.coordinate.file_index() - target_coordinate.file_index(),
        ) == abs(self.coordinate.rank_index() - target_coordinate.rank_index())
