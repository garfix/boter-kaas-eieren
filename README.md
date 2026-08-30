# Boter, kaas en eieren (Tic-tac-toe)

These are just some experiments with problem solving / machine learning, written in Python. The code is mainly writting by AI (Copilot auto, Claude Sonnet 5)

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

## Policies

* Heuristics
* [Minimax](https://nl.wikipedia.org/wiki/Minimax) with [Alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
* [Q-learning](https://en.wikipedia.org/wiki/Q-learning)
* [Monte Carlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)

## Heuristics

Humans play tic-tac-toe using heuristics: (simple) rules that help them win. For example: if the opponent has two marks in a row, put a mark in the position that completes the row.

It's good to mention this policy, because in tic-tac-toe there really are only a few of those rules and they're easy to implement.

## Minimax

Tic-tac-toe is often used to learn about **reinforcement learning**, because it's a simple game. It's so simple that all possible moves and counter-moves can be tried up to the end of the game in real time. And that is what we do here in our Minimax implementation.

Applied to tic-tac-toe, it takes the current state of the board, and for any possible move, checks all possible moves the opponent could make, followed by the moves we could make, and so forth. Up to 8 steps ahead. 

Minimax is really built for games in which each move (or node in the tree) has a quality value. It calculates the path with the best moves for us (max) and the worst moves for the opponent (mini), up to n moves ahead. In the case of tic-tac-toe, there is no use for intermediate scores, and we're also able to calculate all possible outcomes. Therefore we're only interested in immediate moves that eventually lead to success (score: +1), and the ones that eventually lead to failure (score: -1). The others don't matter (score: 0). The move with the highest score is picked.

The most basic implementation doesn't care if we win now or after a few moves. This implementation has a small adaptation that prefers quick wins over later wins.

Note that it uses a single allocated board to learn moves. It changes the board when it moves, and reverts that move when it's done. This saves a lot of time allocating and deallocating memory.

It's easy to apply heuristics to this algorithm, in order to make it faster. One applied here is Alpha-beta pruning, which cuts away pointless branches.

## Q-learning

Q-learning can be applied to **Markov decision processes**, which are characterized by states and actions that move from one state to another. In tic-tac-toe each board configuration (consisting of X's O's and empty spaces) is a state. Adding an X or an O is an action. 5,478 reachable states is a commonly cited number.

In Q-learning each combination of (state, action) is assigned a Q value. Once learning is complete, an agent merely has to check all (state, actions) of a state to find out the best action (taking the maximum of these values). 

In the learning process the agent plays a large number of games against itself (**episodes**). During each game, it starts with X or O, then plays a series of random moves, until it reaches a terminal state. After each move the Q-value of a (state, action) is updated. This is done using a specific formula which basically adjusts the existing value by the Q-value of the next state, modified by a **learning rate** and a **discount factor**. By playing many games, contacting the same (state, action) pairs, the reward assigned to a winning state is propagated back to earlier states and the agent learns the quality of non-terminal (state, action) pairs.

The agent does not only play random moves, actually. Whether it does or not depends on its **exploration_rate**. At the beginning it tries to touch as many states as it can, to have cover much of the search space. Later on, more and more, it just picks the Q value that has been found before. For tic-tac-toe the exploration_rate can be 1 (fully random), but the algorithm for decreasing it is left in, as this code is also meant to illustrate how this might work in real-life RL tasks, where exploring the full search space is impossible and when it is more useful to have accurate information about a smaller part, then to have vage information about a larger part.

Using randomness to explore a search space is never efficient, but the upside is that it can be used without any domain knowledge.

## Monte Carlo Tree Search

Monte Carlo Tree Search (MCTS) explores a limited amount of future game states in a smart way. 

MCTS is suitable for large game spaces where it is not possible to simulate all future states. It just tries the most promising 1000 states or so, then picks the most promising child node.

Of all child states, it **selects** the most promising node first. It **expands** this node into a child node. For this child node node it randomly **simulates** moves until the end of the game, and keeps track of the wins. It does this **iterations** times, and **propagates back** the results from child nodes to parent nodes. then picks the child node (state) with most visits.

Random moves to simuate the rest of the game are great for a simple game like tic-tac-toe, but in a more complex game it is necessary to use heuristics to avoid obvious bad moves.

Deciding with node to explore is based on the Upper Confidence Bound, a balance between **exploration** and **exploitation**. Without exploration, MCTS would just greedily pick the first move that looked okay and never try alternatives. Without exploitation, it would just wander randomly forever.
