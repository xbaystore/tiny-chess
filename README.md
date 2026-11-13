# tiny-chess-01 — a chess engine in 4,077 bytes of Python

Entry for the make.fun bounty **tiny-chess-01** ("Build the strongest chess engine in 4 KB of Python").

`main.py` is a complete chess engine plus the make.fun env client in a single file
(4,077 bytes, Python 3.13, standard library only, no model calls). The shipped file is
self-extracting: an lzma/base85 stub that unpacks the engine source in memory and runs it.

- **Board/moves:** 0x88 board, legal move generation with castling, en passant and promotions.
  Verified by perft against known node counts: startpos depth 3 = 8,902; Kiwipete depth 2 = 2,039
  and depth 3 = 97,862.
- **Search:** negamax alpha-beta with a transposition table (incremental Zobrist hashing),
  null-move pruning, late-move reductions, check extensions, killer/history move ordering with
  MVV-LVA captures, and a quiescence search that resolves captures and check evasions.
  Repetition is detected from the game's own hash history. One fixed budget of 80,000 nodes
  per move — never the clock — stops the search, so play is fully deterministic.
- **Evaluation:** material plus tapered middlegame/endgame piece-square tables in the PeSTO
  style for every piece, blended by game phase, with a bishop-pair bonus.
- **Match loop:** reads `MAKEFUN_ENV_URL`, plays each game to its end and stops cleanly when
  the env reports the game over — no move is ever posted into a finished game.

Local practice gauntlet (the kit's own environment, 8 games against depth- and node-capped
opponents up to Elo ≈ 1,712): **3 wins, 2 draws, 3 losses** — an implied practice Elo of
≈ 1,397, above the house baseline's ≈ 1,325 and the 1,154 qualification floor.

## Run locally

    MAKEFUN_ENV_URL=http://localhost:PORT python3 main.py

With no `MAKEFUN_ENV_URL` set, the program exits immediately.
