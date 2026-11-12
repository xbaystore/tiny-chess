# tiny-chess-01 — a chess engine in 4,080 bytes of Python

Entry for the make.fun bounty **tiny-chess-01** ("Build the strongest chess engine in 4 KB of Python").

`main.py` is a complete chess engine plus the make.fun env client in a single file
(4,080 bytes, Python 3.13, standard library only, no model calls):

- **Board/moves:** 0x88 board, legal move generation with castling, en passant and promotions.
  Verified by perft against known node counts: startpos depth 4 = 197,281; Kiwipete depth 3 = 97,862;
  en-passant-pin position depth 4 = 43,238; CPW positions 4 (9,467) and 5 (62,379) also exact.
- **Search:** negamax alpha-beta with quiescence search (captures + en passant), MVV-LVA move
  ordering with promotion bonuses, two-stage deepening (depth 3, then depth 9) under one fixed
  budget of 20,000 nodes per move.
- **Evaluation:** material plus piece-square tables for pawns and knights (the remaining tables are
  zeroed to fit the byte cap).
- **Deterministic:** the node cap — never the clock — stops the search, so the same position always
  yields the same move (verified in-process and across processes). Worst observed move time ≈ 2 s
  against a 10 s limit.

## Env protocol (as implemented)

The client reads `MAKEFUN_ENV_URL`, then plays up to 64 games:

- `POST /game {}` → expects `{"game": <id>, "fen": <position with our side to move>}`.
- It plays the side to move of that FEN. Each `POST /move {"game": id, "move": uci}` reply is
  expected to carry the new `"fen"` (position after the house reply). If a reply has no `fen`, the
  client applies its own move locally and then stops that game — it never plays the opponent's move.
- `/resign` is never posted: with no legal move the game is already over, and the loop simply ends.

## Run locally

    MAKEFUN_ENV_URL=http://localhost:PORT python3 main.py

With no `MAKEFUN_ENV_URL` set, the program exits immediately.
