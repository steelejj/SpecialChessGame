#!/bin/bash

build() {
  echo "Building docker image..."
  docker build -t special-chess-game .
}

run() {
  echo "Running special chess game"
  docker run special-chess-game
}

# Check the first argument passed to the script
case "$1" in
  build)
    build
    ;;
  run)
    run
    ;;
  *)
    echo "Usage: $0 {build|run}"
    exit 1
    ;;
esac