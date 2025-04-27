import logging
from game.board import ChessBoard
from game.pieces import Rook, Bishop, Coordinate, PieceColor
from logging import getLogger, Logger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
    force=True,
)

def play_game(logger: Logger):
    logger.info("starting game")

    pieces = [
        Rook(color=PieceColor.BLACK, coordinate=Coordinate("A", 2)),
        Bishop(color=PieceColor.WHITE, coordinate=Coordinate("G", 8))
    ]

    board = ChessBoard(pieces=pieces, board_size=8, logger=logger)

    board.render()

if __name__ == "__main__":
    game_logger = getLogger("ChessGame")
    play_game(game_logger)
