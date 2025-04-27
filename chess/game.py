from logging import Logger
from typing import Optional

from chess.board import ChessBoard
from chess.move import toss_coin, roll_dice
from chess.pieces import Bishop, Rook, ChessPiece


class Game:
    def __init__(self, rook: Rook, bishop: Bishop, logger: Logger, board_size: int = 8):
        self.rook = rook
        self.bishop = bishop
        self.logger = logger
        self.board_size = board_size
        self.board = ChessBoard(pieces=[rook, bishop], board_size=self.board_size, logger=self.logger)
        self.winner: Optional[ChessPiece] = None

    def play_turn(self):
        rook_direction = toss_coin()
        rook_move_spaces = roll_dice() + roll_dice()
        current_position = self.rook.coordinate
        self.rook.move(direction=rook_direction, spaces=rook_move_spaces, board_size=self.board_size)
        self.logger.info(f"Rook on {current_position} moved {rook_direction.value} {rook_move_spaces} spaces to {self.rook.coordinate}")
        if self.bishop.can_capture(self.rook.coordinate):
            self.logger.info(f"The bishop on {self.bishop.coordinate} can capture the rook on {self.rook.coordinate} and wins the game")
            self.winner = self.bishop
        elif self.rook.can_capture(self.bishop.coordinate):
            self.logger.info(f"The rook on {self.rook.coordinate} can capture the bishop on {self.bishop.coordinate} and wins the game")
            self.winner = self.rook
        else:
            self.logger.info(f"The rook on {self.rook.coordinate} and the bishop on {self.bishop.coordinate} cannot capture each other")

    def play_game(self, number_of_turns: int):
        self.logger.info("Starting game")
        current_turn = 1
        self.board.render()
        while not self.winner and current_turn <= number_of_turns:
            self.logger.info(f"Playing turn {current_turn}")
            self.play_turn()
            self.board.render()
            current_turn += 1

        self.winner = self.rook
        self.logger.info(f"The winner is {self.winner}")



