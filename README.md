# Boter, kaas en eieren

A small Python command-line game and a clean starting point for experimenting with CLI games.

## Quick start

Install the project and development tools with [uv](https://docs.astral.sh/uv/):

```console
uv sync
uv run boter-kaas-eieren
```

Run the checks:

```console
uv run pytest
uv run ruff check .
```

The game engine lives in `src/boter_kaas_eieren/game.py`, separate from terminal input and output in `cli.py`. That makes it straightforward to add a computer opponent, a different board size, or a new interface later.
