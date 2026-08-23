# Boter, kaas en eieren

These are just some experiments with problem solving / machine learning. The code is mainly writting by AI (Copilot auto, Claude Sonnet 5)

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

## Models

* [Minimax](https://nl.wikipedia.org/wiki/Minimax) with [Alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
* [QLearning](https://en.wikipedia.org/wiki/Q-learning)

