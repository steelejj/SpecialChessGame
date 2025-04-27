import copy
from functools import cached_property
from logging import Logger

from chess.pieces import ChessPiece


class ChessBoard:
    def __init__(self, pieces: list[ChessPiece], board_size: int, logger: Logger) -> None:
        self.pieces: list[ChessPiece] = pieces
        self._board_size = board_size
        self.logger = logger
        self.validate()

    def validate(self):
        coordinates = [piece.coordinate for piece in self.pieces]

        if len(set(coordinates)) != len(coordinates):
            raise ValueError("input coordinates must be unique, make sure all pieces start at different positions")


    @cached_property
    def _empty_board(self) -> list[list[str]]:
        return [["_" for _ in range(self._board_size)] for _ in range(self._board_size)]

    def _populate_board(self) -> list[list[str]]:
        board = copy.deepcopy(self._empty_board)
        for piece  in self.pieces:
            board[piece.coordinate.rank_index()][piece.coordinate.file_index()] = piece.emoji

        return board

    def render(self) -> None:
        self.logger.info("Rendering the current state of board")

        formatted = ""
        for row in self._populate_board():
            formatted += "  ".join(row) + "\n"

        self.logger.info("\n" + formatted)
