from functools import cached_property
from logging import Logger
from typing import List
from game.pieces import ChessPiece

class ChessBoardBuilder:
    def __init__(self, board: List[List[ChessPiece]]):

class ChessBoard:
    def __init__(self, pieces: List[ChessPiece], logger: Logger, board_size: int = 8) -> None:
        self._board_size = board_size  # Use board_size parameter

        # self.pieces = pieces
        # self.logger = logger
        # self.board_state: List[List[str]] = self._init_board_state()

    def get_board_state(self) -> List[List[str]]:


    def _empty_board(self) -> List[List[str]]:
        return [["_" for _ in range(self._board_size)] for _ in range(self._board_size)]

    def _init_board_state(self) -> list[list[str]]:
        board = self._empty_board()
        for piece in self.pieces:
            board[piece.coordinate.rank_index()][piece.coordinate.file_index()] = piece.emoji

        return board

    def render(self) -> None:
        self.logger.info("Rendering the current state of board")

        formatted = ""
        for row in self.board_state:
            formatted += "  ".join(row) + "\n"

        self.logger.info("\n" + formatted)
