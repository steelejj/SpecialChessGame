from logging import Logger
from typing import Optional

from chess.board import ChessBoard
from chess.move import roll_dice, toss_coin
from chess.pieces import Bishop, ChessPiece, Rook


class Game:
    """
    Manages a chess game between a rook and a bishop.

    Attributes:
    ----------
        rook (Rook): The rook piece.
        bishop (Bishop): The bishop piece.
        logger (Logger): Logger for game events.
        board_size (int): The size of the chessboard.
        board (ChessBoard): The chessboard instance containing the pieces.
    """

    def __init__(
        self,
        rook: Rook,
        bishop: Bishop,
        logger: Logger,
        board_size: int = 8,
    ) -> None:
        """
        Initialize the game with a rook, bishop, logger, and board size.

        Args:
        ----
            rook (Rook): The rook piece.
            bishop (Bishop): The bishop piece.
            logger (Logger): Logger for game events.
            board_size (int, optional): Size of the chessboard. Defaults to 8.
        """
        self.rook = rook
        self.bishop = bishop
        self.logger = logger
        self.board_size = board_size
        self.board = ChessBoard(
            pieces=[rook, bishop],
            board_size=self.board_size,
            logger=self.logger,
        )

    def _play_turn(self) -> ChessPiece | None:
        """
        Execute a single turn for both pieces.

        The rook attempts to capture the bishop first; if it fails, it moves based on
        a coin toss and two dice rolls. Then the bishop attempts to capture the rook.

        Returns:
        -------
            ChessPiece | None: The piece that captured its opponent this turn,
            or None if no capture occurred.
        """
        # if the rook can capture the bishop it does and wins the game, if not then move the rook
        if self.rook.can_capture(self.bishop.coordinate):
            self.logger.info(
                f"The rook on {self.rook.coordinate} can capture the bishop on {self.bishop.coordinate}.",
            )
            return self.rook
        else:
            rook_direction = toss_coin()
            rook_move_spaces = roll_dice() + roll_dice()
            current_position = self.rook.coordinate
            self.logger.info(
                f"The rook on {current_position} cannot capture the bishop on {self.bishop.coordinate}.",
            )
            self.rook.move(
                direction=rook_direction,
                spaces=rook_move_spaces,
                board_size=self.board_size,
            )
            self.logger.info(
                f"Rook on {current_position} moves {rook_direction.value} {rook_move_spaces} spaces to {self.rook.coordinate}",
            )

        # if the bishop can capture the rook after it moves it wins the game
        if self.bishop.can_capture(self.rook.coordinate):
            self.logger.info(
                f"The bishop on {self.bishop.coordinate} can capture the rook on {self.rook.coordinate}.",
            )
            return self.bishop
        else:
            self.logger.info(
                f"The bishop on {self.bishop.coordinate} cannot capture the rook on {self.rook.coordinate}.",
            )
            return None

    def play_game(self, number_of_turns: int) -> tuple[ChessPiece, int]:
        """
        Play the game up to a maximum number of turns.

        Logs each turn, renders the board, and stops early if a capture occurs.

        Args:
        ----
            number_of_turns (int): Maximum number of turns to play.

        Returns:
        -------
            tuple[ChessPiece, int]: A tuple containing the winning piece (or the rook by default
            if no capture occurred) and the turn count at which the game ended.
        """
        self.logger.info("Starting game")
        current_turn = 1
        self.board.render()

        maybe_winner: Optional[ChessPiece] = None

        while not maybe_winner and current_turn <= number_of_turns:
            self.logger.info(f"Playing turn {current_turn}")
            maybe_winner = self._play_turn()
            self.board.render()
            if not maybe_winner:
                current_turn += 1

        return self.rook if not maybe_winner else maybe_winner, current_turn
