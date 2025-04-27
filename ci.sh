#!/usr/bin/env bash
set -e

IMAGE="special-chess-game"

build() {
  echo "📦 Building Docker image..."
  docker build -t $IMAGE .
}

run() {
  echo "▶️  Running special chess game"
  docker run --rm $IMAGE
}

lint() {
  echo "🔍 Linting with Ruff inside container…"
  docker run --rm \
    -v "$(pwd)":/app \
    -w /app \
    $IMAGE \
    ruff python/src
}

type_check() {
  echo "🧩 Type‐checking with Mypy inside container…"
  docker run --rm \
    -v "$(pwd)":/app \
    -w /app \
    -e PYTHONPATH="/app/python/src:${PYTHONPATH}" \
    $IMAGE \
    mypy python/src
}

check() {
  echo "✅ Running full check (lint + type_check)…"
  lint
  type_check
  echo "🎉 All checks passed!"
}

case "$1" in
  build)       build      ;;
  run)         run        ;;
  lint)        lint       ;;
  type_check)  type_check ;;
  check)       check      ;;
  *)
    cat <<-EOF
    Usage: $0 {build|run|lint|type_check|check}

      build       Build the Docker image
      run         Run the Chess game in Docker
      lint        Run (ruff) linter inside container
      type_check  Run (mypy) static type checks inside container
      check       Run both lint & type_check
    EOF
    exit 1
    ;;
esac
