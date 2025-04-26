import logging
from game.board import ChessBoard
from game.pieces import Rook, Bishop, Coordinate
from logging import getLogger, Logger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
    force=True,
)

def play_game(logger: Logger):
    logger.info("starting game")            # <-- now this will show
    pieces = [
        Rook(Coordinate('g',8)),
        Bishop(Coordinate('b',7))
    ]
    board = ChessBoard(pieces, logger=logger)
    board.render()

if __name__ == "__main__":
    game_logger = getLogger("ChessGame")
    play_game(game_logger)
