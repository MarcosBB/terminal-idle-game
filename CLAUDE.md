# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A terminal-based idle/incremental game (like Cookie Clicker) built in Python. The player buys properties (farmer, cow, plantation, etc.) that generate passive income, rendered as a `rich` table refreshed in a loop, with `pynput` capturing keypresses.

## Commands

Requires Python 3.12.3. A `.venv` already exists in the repo; activate it or install requirements yourself:

```bash
pip install -r requirements.txt
```

Run the game:
```bash
python3 main.py
```

Run the game with a fresh save (skips loading `savegame.json`):
```bash
python3 main.py --reset
```

Run all tests:
```bash
python3 -m unittest
```

Run a single test file / case:
```bash
python3 -m unittest tests.test_game
python3 -m unittest tests.test_game.GameTestCase.test_it_should_buy_property_correctly
```

Format code (black is a dependency, used per commit history — e.g. "running black"):
```bash
black .
```

Coverage:
```bash
coverage run -m unittest discover
coverage report
coverage html   # then open htmlcov/index.html
```

Mutation testing (cosmic-ray, configured in `crconfig.toml` against `src/game.py`):
```bash
cosmic-ray init crconfig.toml cr.sqlite
cosmic-ray exec crconfig.toml cr.sqlite
cr-html cr.sqlite > report.html
```

## Architecture

Three modules under `src/`, wired together by `main.py`:

- **`src/configs.py`** — all tunable constants and the default game state: `DEFAULT_MONEY`, `DEFAULT_PROPERTIES` (list of property dicts with `name`/`value`/`income`/`quantity`/`money_per_second`), `MULTIPLIER_OPTIONS` (`[1, 10, 100, "Max"]`), `MAX_VALUE` (the sentinel string `"Max"` used as a multiplier option), `SAVE_FILE_PATH` (default `savegame.json`), and `FRAMES_PER_SECOND`/`SECONDS_PER_FRAME` which drive the game loop timing.
- **`src/game.py`** — `Game` holds all game state and mutation logic: `earn_money` (called every frame, scales by `SECONDS_PER_FRAME`), `buy_property` (quantity depends on the current multiplier; `"Max"` computes the largest affordable batch via floor division), `update_money_per_second`/`update_money_per_second_by_property`, `change_multiplier` (cycles through `multiplier_options`, wrapping to 0), and the `get_multiplier` property. `Game.__init__` also takes a `save_file_path` (default `SAVE_FILE_PATH`), so tests can point it at a temp file. `save()` writes `money`, `multiplier_index`, and a `{property_name: quantity}` dict to that JSON file; `load()` reads it back and applies saved quantities by matching property **name** (not list position), so a save survives economy rebalances or new properties being added to `DEFAULT_PROPERTIES` — missing/corrupt save files are silently ignored rather than raising.
- **`src/menu.py`** — `Menu` is purely presentational: builds the header string (money, money/sec, current multiplier) and a `rich.table.Table` of properties from `Game` state, formatting numbers with `numerize`. It does not mutate `Game`.
- **`main.py`** — wires `Game` and `Menu` together. Parses a `--reset` CLI flag (via `argparse`); when absent, calls `game.load()` right after constructing `Game` and before constructing `Menu`, so the loaded state is reflected in the first render. Registers a `pynput.keyboard.Listener` (`on_press`) that maps number keys to `buy_property(index)`, `x` to `change_multiplier`, `s` to `save`. Runs an infinite loop that clears the terminal (`os.system("clear")`), advances game state (`earn_money`), redraws the menu, and sleeps to hold the frame rate at `SECONDS_PER_FRAME`, tracking `frame_rate_problem` if a frame overruns its budget.

Key coupling to be aware of: property dicts are shared mutable state — `Game` mutates the `quantity`/`money_per_second` fields in place, and `Menu` reads those same dicts directly (no copying/DTOs). Tests in `tests/` construct their own property lists rather than relying on `DEFAULT_PROPERTIES`, since `Game`'s default argument is mutable and shared across instantiations if not overridden explicitly. Progress is only persisted when the player presses `s` (or code calls `game.save()` directly) — there's no autosave, and `--reset` just skips `load()` rather than deleting the save file, so an old save on disk is still overwritten the next time `save()` runs.

## Testing conventions

- Uses stdlib `unittest` (not pytest) plus `parameterized.expand` for table-driven cases (see `tests/test_game.py`).
- Each test's `setUp` constructs a fresh `Game`/`Menu` with an explicit small property list — don't rely on `DEFAULT_PROPERTIES` in new tests, to avoid mutable-default sharing across tests.
- Save/load tests (`tests/test_game.py`) point `Game(save_file_path=...)` at a `tempfile`-generated path in `setUp` and remove it in `tearDown`, so tests never touch the real `savegame.json`.
- `.coveragerc` omits `tests/`, `test_*.py`, and `__init__.py` from coverage reports.
