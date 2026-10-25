# Dark River Tavern Menu: figure brief

Goal: one picture per tile of the Crispy Fried Chicken Status Board. Each picture lays out the tile's actual data and
shows how and why the tile passes, fails or stays open. The pictures go on a menu-style web page.

## Inputs
- Tile list: `explainers/dark_river_tavern_menu/board_tiles.json` (40 tiles; `col`, `name`, `st` status, `note`, `lanes`).
  The board is `explainers/img/status_board.png` (v3s, 23 Oct 2026), drawn by `explainers/make_status_board.py`.
- Lane ids map to directories: `rebuild_2026_10_22/<ID>_*` (C5, C8, P3, P4, S1–S4, U1, X3, H4, Q6, Q7, M1, M2, J1, K1,
  T1, N0, F1–F3, I1, X9, X11, X13, ...); `campaign_fresh_gravity/CFG<nnn>_*` for CFG ids; others via
  `grep -rl` / `find . -maxdepth 3 -type d -name "<ID>*"`. `rebuild_2026_10_22/N0_board_audit/AUDIT.md` says which lane
  carries the evidence for each tile. Prefer `*_results.json`, `*.out`, `.csv`, `.npz` in the lane directory.

## Output (write ONLY inside `explainers/dark_river_tavern_menu/`)
1. `scripts/col<N>_figs.py`: imports `menu_style` (same folder; read it) and draws every tile of your column(s),
   one PNG each via `menu_style.finish(fig, slug, status, title, verdict, source)`. Slug: `c<col>_<two-digit index
   within column, from board order>_<short_snake_name>`. Status key: PASS / COND / UNDEC / FAIL / OPEN (use OPEN for
   the grey "not yet recomputed" tile). Run it: `python3 -I scripts/col<N>_figs.py` from that folder, or with
   `sys.path` set so menu_style imports.
2. `captions/col<N>.json`: list of {slug, name, status, data (what was measured, which sample), picture (what the
   reader sees: axes, points, line, band), why (2–4 plain sentences: how it passes or fails and why), numbers (the
   key numbers, each with its file), sources [{path, commit}] (commit via `git log -1 --format=%h -- <path>`)}.
3. Look at every PNG you made (Read tool) and fix anything unreadable or clipped.

## Picture rules
- Plot the real data from committed files: measured points with error bars against the framework's prediction
  (line or band), with the pass line or threshold drawn. Mark failures where the data leave the band.
- For theory tiles with no data arrays (health, causality, kappa, ...): draw a scale or bar diagram of the key
  quantities against the threshold that decides the tile (e.g. a log axis: bound vs prediction), or a small
  labelled schematic of the condition. Keep it truthful and simple.
- Every number in a picture or caption must be read from a committed file. Never invent, eyeball or round
  differently from the file. If you cannot find a number in a file, leave it out and say so in `why`.
- 🛑 Owner rule: ΛCDM is not a yardstick. Never plot ΛCDM curves, ΛCDM fits or "vs ΛCDM" Δχ² as the comparison.
  Raw data against the framework's own prediction only. If a lane's verdict used a ΛCDM-derived input (e.g. the
  Planck abundance Ω_c/Ω_b = 5.364, a flat-ΛCDM growth background), say so in `why` as an inherited input.
- Wording: κ = ½ is FITTED; the two footings (canonical 9.3603e-11, alt 1.1312e-10 m/s²) are never pooled (show
  both or say which); never "theory closed"; never say the data favour the framework or any rival; the cold
  component is "cold dark energy" (or "cold dust" where a lane says so), never "cold dark matter".
- Tile status and colour come from the board as is. Do not recolour.

## Limits
- Plotting and reading only. No new physics runs, no reruns of lane scripts that take more than a minute or 1 GB
  (a long simulation is running on this machine). Single thread.
- Do not edit, move or commit anything outside `explainers/dark_river_tavern_menu/`. Do not git commit.
- Final report: a short list, one line per tile: slug, done / partial (what is missing), and anything you doubt.
