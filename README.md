# Special Chess Game

## Summary

This is a special chess game between a bishop and a rook. The game flows as follows:
- Game starts with the rook on H1 and the Bishop on C3
- For each turn:
  - the rook captures the bishop if it can, and wins the game
  - If the rook can't capture the bishop, it makes a random move between 1 and 12 spaces (wrapping around the board) either up or to the right
  - After the rook moves, if the bishop can capture the rook, it wins the game
- After 15 turns, if neither piece has been captured, the game ends and the rook wins

## How to Run
### Dependencies
- docker

### Building the app
Required prior to running
```bash
ci.sh build
```

### Running the app
```bash
./ci.sh run
```

### Run Unit Tests
```bash
./ci.sh test
```

### Run black, ruff, and mypy
These will autofix when available
```bash
./ci.sh check
```


## Assumptions / Decisions
- The board does not have to maintain any state, all state is contained within the pieces
- The rook always tries to capture at the beginning of its turn
- The bishop always tries to capture at the end of its turn
- A turn consists of the rook trying to capture, moving, and the bishop trying to capture
- The rook wins by default after 15 turns
- The rook can only move up or to the right
- The bishop never has to move
- There are no additional pieces on the board