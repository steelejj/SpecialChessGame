import copy
from functools import cached_property
from logging import Logger

from chess.pieces import ChessPiece


class ChessBoard:
    """Represents a chessboard containing multiple chess pieces.

    Attributes:
        pieces (list[ChessPiece]): The list of chess pieces on the board.
        _board_size (int): The size of the board (number of ranks/files).
        logger (Logger): Logger for rendering and validation messages.
    """

    def __init__(self, pieces: list[ChessPiece], board_size: int, logger: Logger) -> None:
        """Initialize the ChessBoard with pieces, size, and logger, then validate.

        Args:
            pieces (list[ChessPiece]): The chess pieces to place on the board.
            board_size (int): The dimension of the board (e.g., 8 for 8x8).
            logger (Logger): Logger for game events and rendering.

        Raises:
            ValueError: If pieces have duplicate coordinates.
        """
        self.pieces: list[ChessPiece] = pieces
        self._board_size = board_size
        self.logger = logger
        self.validate()

    def validate(self):
        """Ensure all pieces occupy unique coordinates.

        Raises:
            ValueError: If any two pieces share the same coordinate.
        """
        coordinates = [piece.coordinate for piece in self.pieces]

        if len(set(coordinates)) != len(coordinates):
            raise ValueError("input coordinates must be unique, make sure all pieces start at different positions")

    @cached_property
    def _empty_board(self) -> list[list[str]]:
        """Create and cache an empty board grid.

        Returns:
            list[list[str]]: A 2D list representing an empty board with "_" in each cell.
        """
        return [["_" for _ in range(self._board_size)] for _ in range(self._board_size)]

    def _populate_board(self) -> list[list[str]]:
        """Populate the empty board grid with piece emojis.

        Returns:
            list[list[str]]: A 2D list representing the board with piece emojis placed at their coordinates.
        """
        board = copy.deepcopy(self._empty_board)
        for piece in self.pieces:
            board[piece.coordinate.rank_index()][piece.coordinate.file_index()] = piece.emoji

        return board

    def render(self) -> None:
        """Render the current state of the board via the logger.

        Logs the board with rows joined by two spaces, preceded by a rendering message.
        """
        self.logger.info("Rendering the current state of board")

        formatted = ""
        for row in self._populate_board():
            formatted += "  ".join(row) + "\n"

        self.logger.info("\n" + formatted)
