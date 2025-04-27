import logging
from logging import getLogger

from chess.game import Game
from chess.pieces import Bishop, Coordinate, PieceColor, Rook

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
    force=True,
)

if __name__ == "__main__":
    game_logger = getLogger("ChessGame")
    rook = Rook(coordinate=Coordinate("H", 1), color=PieceColor.WHITE)
    bishop = Bishop(coordinate=Coordinate("C", 3), color=PieceColor.BLACK)
    number_of_turns = 15

    game = Game(rook=rook, bishop=bishop, logger=game_logger)
    result, number_of_turns = game.play_game(number_of_turns=number_of_turns)

    game_logger.info(f"The {result} wins in {number_of_turns} turns")
