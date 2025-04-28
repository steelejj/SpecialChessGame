#!/usr/bin/env bash
set -e

IMAGE="special-chess-game"

build() {
  echo "📦 Building Docker image..."
  docker build -t "$IMAGE" .
}

run() {
  echo "▶️  Running special chess game"
  docker run --rm "$IMAGE"
}

ruff() {
  echo "🔍 Linting with Ruff inside container…"
  docker run --rm \
    -v "$(pwd)":/app \
    -w /app \
    "$IMAGE" \
    ruff check --fix python/src
}

black() {
  echo "🔍 Formatting with Black inside container…"
  docker run --rm \
    -v "$(pwd)":/app \
    -w /app \
    "$IMAGE" \
    black python
}

type_check() {
  echo "🧩 Type-checking with Mypy inside container…"
  docker run --rm \
    -v "$(pwd)":/app \
    -w /app \
    -e PYTHONPATH="/app/python/src:${PYTHONPATH}" \
    "$IMAGE" \
    mypy python/src
}

check() {
  echo "✅ Running full check (ruff + type_check)…"
  black
  ruff
  type_check
  echo "🎉 All checks passed!"
}

usage() {
  echo "Usage: $0 {build|run|ruff|type_check|check}"
  exit 1
}

# if no argument given, show usage
[ $# -eq 0 ] && usage

case "$1" in
  build)       build      ;;
  run)         run        ;;
  ruff)        ruff       ;;
  black)       black      ;;
  type_check)  type_check ;;
  check)       check      ;;
  *)            usage     ;;
esac
